# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx",
# ]
# ///
"""Scan a directory and upload files to an Open WebUI knowledge base.

Usage:
    uv run upload_to_knowledge.py <directory> --api-key <key> [--knowledge-name <name>] [--base-url <url>]

The script will:
1. Create a knowledge base (or reuse an existing one by name)
2. Upload all files from the directory
3. Wait for processing to complete
4. Add each file to the knowledge base
"""

import argparse
import sys
import time
from pathlib import Path

import httpx

DEFAULT_BASE_URL = "http://localhost:3000"
POLL_INTERVAL = 2
POLL_TIMEOUT = 300


def get_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }


def find_or_create_knowledge(
    client: httpx.Client, name: str, headers: dict
) -> str:
    resp = client.get("/api/v1/knowledge/", headers=headers)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("items", data) if isinstance(data, dict) else data
    for kb in items:
        if kb["name"] == name:
            print(f"Using existing knowledge base: {name} (id={kb['id']})")
            return kb["id"]

    resp = client.post(
        "/api/v1/knowledge/create",
        headers={**headers, "Content-Type": "application/json"},
        json={"name": name, "description": f"Auto-uploaded from directory"},
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
            resp = client.get(
                f"/api/v1/files/{file_id}",
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
            # Check if file has content extracted (meta.collection_name is set when done)
            meta = data.get("meta", {})
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


def scan_directory(directory: Path) -> list[Path]:
    files = sorted(f for f in directory.iterdir() if f.is_file())
    if not files:
        print(f"No files found in {directory}")
        sys.exit(1)
    return files


def main():
    parser = argparse.ArgumentParser(
        description="Upload files from a directory to Open WebUI knowledge base"
    )
    parser.add_argument("directory", type=Path, help="Directory to scan for files")
    parser.add_argument("--api-key", required=True, help="Open WebUI API key")
    parser.add_argument(
        "--knowledge-name",
        default=None,
        help="Knowledge base name (default: directory name)",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Open WebUI base URL (default: {DEFAULT_BASE_URL})",
    )
    args = parser.parse_args()

    directory = args.directory.resolve()
    if not directory.is_dir():
        print(f"Error: {directory} is not a directory")
        sys.exit(1)

    knowledge_name = args.knowledge_name or directory.name
    headers = get_headers(args.api_key)
    files = scan_directory(directory)
    print(f"Found {len(files)} file(s) in {directory}")

    with httpx.Client(base_url=args.base_url, timeout=120) as client:
        knowledge_id = find_or_create_knowledge(client, knowledge_name, headers)

        for filepath in files:
            print(f"\nProcessing: {filepath.name}")
            file_id = upload_file(client, filepath, headers)
            wait_for_processing(client, file_id, filepath.name, headers)
            add_file_to_knowledge(client, knowledge_id, file_id, headers)
            print(f"  Added to knowledge base: {filepath.name}")

    print(f"\nDone! {len(files)} file(s) added to knowledge base '{knowledge_name}'")


if __name__ == "__main__":
    main()
