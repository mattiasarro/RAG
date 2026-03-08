# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx",
# ]
# ///
"""Incrementally sync a versioned directory to an Open WebUI knowledge base.

Usage:
    uv run scripts/update_knowledge.py data/versioned/et_wiki_10 --api-key <key>

Expects a directory structure like:
    data/versioned/et_wiki_10/
        2026-03-07/
        2026-03-08/
        _sync_log.csv

The script finds the latest subdirectory (by name sort) and syncs it:
- If the knowledge base doesn't exist, creates it and uploads all files.
- If it exists, reads _sync_log.csv to find the last completed sync dir,
  then diffs the two directories (added/removed/modified files by md5).

Appends a row to _sync_log.csv after each run.
"""

import argparse
import csv
import hashlib
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

DEFAULT_BASE_URL = "http://localhost:3000"
POLL_INTERVAL = 2
POLL_TIMEOUT = 300
SYNC_LOG_NAME = "_sync_log.csv"


def get_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }


def md5(filepath: Path) -> str:
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def file_hashes(directory: Path) -> dict[str, str]:
    return {f.name: md5(f) for f in sorted(directory.iterdir()) if f.is_file()}


def find_latest_subdir(base: Path) -> Path:
    subdirs = sorted(
        [d for d in base.iterdir() if d.is_dir()],
        key=lambda d: d.name,
    )
    if not subdirs:
        print(f"Error: no subdirectories found in {base}")
        sys.exit(1)
    return subdirs[-1]


def find_knowledge(client: httpx.Client, name: str, headers: dict) -> str | None:
    resp = client.get("/api/v1/knowledge/", headers=headers)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("items", data) if isinstance(data, dict) else data
    for kb in items:
        if kb["name"] == name:
            return kb["id"]
    return None


def create_knowledge(client: httpx.Client, name: str, headers: dict) -> str:
    resp = client.post(
        "/api/v1/knowledge/create",
        headers={**headers, "Content-Type": "application/json"},
        json={"name": name, "description": f"Auto-synced from versioned directory"},
    )
    resp.raise_for_status()
    kb_id = resp.json()["id"]
    print(f"Created knowledge base: {name} (id={kb_id})")
    return kb_id


def upload_file(client: httpx.Client, filepath: Path, headers: dict) -> str:
    with open(filepath, "rb") as f:
        resp = client.post(
            "/api/v1/files/",
            headers=headers,
            files={"file": (filepath.name, f)},
            timeout=120,
        )
    resp.raise_for_status()
    file_id = resp.json()["id"]
    print(f"  Uploaded: {filepath.name} (id={file_id})")
    return file_id


def wait_for_processing(
    client: httpx.Client, file_id: str, filename: str, headers: dict
) -> bool:
    deadline = time.monotonic() + POLL_TIMEOUT
    while time.monotonic() < deadline:
        try:
            resp = client.get(f"/api/v1/files/{file_id}", headers=headers)
            resp.raise_for_status()
            meta = resp.json().get("meta", {})
            if meta.get("collection_name"):
                return True
        except httpx.HTTPStatusError:
            pass
        time.sleep(POLL_INTERVAL)
    print(f"  WARNING: Timed out waiting for {filename} to process")
    return False


def add_file_to_knowledge(
    client: httpx.Client, knowledge_id: str, file_id: str, headers: dict
):
    resp = client.post(
        f"/api/v1/knowledge/{knowledge_id}/file/add",
        headers={**headers, "Content-Type": "application/json"},
        json={"file_id": file_id},
    )
    resp.raise_for_status()


def get_kb_files(client: httpx.Client, knowledge_id: str, headers: dict) -> dict[str, str]:
    """Return {filename: file_id} for all files in the knowledge base."""
    resp = client.get("/api/v1/files/", headers=headers)
    resp.raise_for_status()
    all_files = resp.json()
    return {
        f["filename"]: f["id"]
        for f in all_files
        if (f.get("meta") or {}).get("collection_name") == knowledge_id
    }


def remove_file_from_knowledge(
    client: httpx.Client, knowledge_id: str, file_id: str, headers: dict
):
    resp = client.post(
        f"/api/v1/knowledge/{knowledge_id}/file/remove",
        headers={**headers, "Content-Type": "application/json"},
        json={"file_id": file_id},
    )
    resp.raise_for_status()


def delete_file(client: httpx.Client, file_id: str, headers: dict):
    resp = client.delete(f"/api/v1/files/{file_id}", headers=headers)
    resp.raise_for_status()


def upload_and_add(
    client: httpx.Client, filepath: Path, knowledge_id: str, headers: dict
):
    file_id = upload_file(client, filepath, headers)
    wait_for_processing(client, file_id, filepath.name, headers)
    add_file_to_knowledge(client, knowledge_id, file_id, headers)
    print(f"  Added to knowledge base: {filepath.name}")


def remove_and_delete(
    client: httpx.Client,
    filename: str,
    knowledge_id: str,
    kb_files: dict[str, str],
    headers: dict,
):
    file_id = kb_files.get(filename)
    if not file_id:
        print(f"  WARNING: {filename} not found in knowledge base, skipping removal")
        return
    remove_file_from_knowledge(client, knowledge_id, file_id, headers)
    print(f"  Removed from knowledge base: {filename}")


def read_last_completed_dir(sync_log: Path) -> str | None:
    if not sync_log.exists():
        return None
    with open(sync_log) as f:
        reader = csv.DictReader(f)
        last_completed = None
        for row in reader:
            if row["status"] == "completed":
                last_completed = row["dir"]
    return last_completed


def append_sync_log(sync_log: Path, dir_name: str, status: str):
    write_header = not sync_log.exists()
    with open(sync_log, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["dir", "timestamp", "status"])
        writer.writerow([dir_name, datetime.now(timezone.utc).isoformat(), status])


def main():
    parser = argparse.ArgumentParser(
        description="Incrementally sync a versioned directory to Open WebUI knowledge base"
    )
    parser.add_argument(
        "directory", type=Path, help="Versioned directory (e.g. data/versioned/et_wiki_10)"
    )
    parser.add_argument("--api-key", required=True, help="Open WebUI API key or JWT token")
    parser.add_argument(
        "--knowledge-name", default=None, help="Knowledge base name (default: directory name)"
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Open WebUI base URL (default: {DEFAULT_BASE_URL})",
    )
    args = parser.parse_args()

    base_dir = args.directory.resolve()
    if not base_dir.is_dir():
        print(f"Error: {base_dir} is not a directory")
        sys.exit(1)

    knowledge_name = args.knowledge_name or base_dir.name
    headers = get_headers(args.api_key)
    sync_log = base_dir / SYNC_LOG_NAME
    latest_dir = find_latest_subdir(base_dir)
    previous_dir_name = read_last_completed_dir(sync_log)

    if previous_dir_name == latest_dir.name:
        print(f"Already up to date — {latest_dir.name} was already synced")
        return

    latest_files = file_hashes(latest_dir)
    print(f"Latest directory: {latest_dir.name} ({len(latest_files)} files)")

    status = "failed"
    try:
        with httpx.Client(base_url=args.base_url, timeout=120) as client:
            kb_id = find_knowledge(client, knowledge_name, headers)

            if kb_id is None:
                # Fresh knowledge base — upload everything
                kb_id = create_knowledge(client, knowledge_name, headers)
                for filename in latest_files:
                    print(f"\nAdding: {filename}")
                    upload_and_add(client, latest_dir / filename, kb_id, headers)
                print(f"\nDone! Uploaded {len(latest_files)} file(s)")
            else:
                print(f"Using existing knowledge base: {knowledge_name} (id={kb_id})")
                if previous_dir_name is None:
                    print("Error: knowledge base exists but no completed sync in _sync_log.csv")
                    sys.exit(1)

                previous_dir = base_dir / previous_dir_name
                if not previous_dir.is_dir():
                    print(f"Error: previous sync dir {previous_dir} does not exist")
                    sys.exit(1)

                previous_files = file_hashes(previous_dir)
                kb_files = get_kb_files(client, kb_id, headers)

                added = set(latest_files) - set(previous_files)
                removed = set(previous_files) - set(latest_files)
                common = set(latest_files) & set(previous_files)
                modified = {f for f in common if latest_files[f] != previous_files[f]}
                unchanged = common - modified

                print(f"\nDiff: +{len(added)} added, -{len(removed)} removed, "
                      f"~{len(modified)} modified, ={len(unchanged)} unchanged")

                for filename in sorted(removed):
                    print(f"\nRemoving: {filename}")
                    remove_and_delete(client, filename, kb_id, kb_files, headers)

                for filename in sorted(modified):
                    print(f"\nUpdating: {filename}")
                    remove_and_delete(client, filename, kb_id, kb_files, headers)
                    upload_and_add(client, latest_dir / filename, kb_id, headers)

                for filename in sorted(added):
                    print(f"\nAdding: {filename}")
                    upload_and_add(client, latest_dir / filename, kb_id, headers)

                print(f"\nDone! Sync complete for {latest_dir.name}")

            status = "completed"
    finally:
        append_sync_log(sync_log, latest_dir.name, status)
        print(f"Logged: {latest_dir.name} -> {status}")


if __name__ == "__main__":
    main()
