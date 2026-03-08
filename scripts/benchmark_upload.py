# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx",
# ]
# ///

"""Benchmark upload speed by sampling n random files from a directory.

Usage:
    uv run benchmark_upload.py <directory> --n <count> --api-key <key> [--base-url <url>]

The script will:
1. Sample n random files from the directory
2. Copy them to a temporary directory
3. Upload them via upload_to_knowledge.py
4. Report elapsed time and estimate total time for the full directory
"""

import argparse
import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import httpx


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark upload speed by sampling random files"
    )
    parser.add_argument("directory", type=Path, help="Directory to sample files from")
    parser.add_argument(
        "--n", type=int, required=True, help="Number of files to sample"
    )
    parser.add_argument("--api-key", required=True, help="Open WebUI API key")
    parser.add_argument(
        "--base-url",
        default="http://localhost:3000",
        help="Open WebUI base URL (default: http://localhost:3000)",
    )
    args = parser.parse_args()

    directory = args.directory.resolve()
    if not directory.is_dir():
        print(f"Error: {directory} is not a directory")
        sys.exit(1)

    all_files = sorted(f for f in directory.iterdir() if f.is_file())
    total_count = len(all_files)
    if total_count == 0:
        print(f"Error: no files found in {directory}")
        sys.exit(1)

    n = args.n
    if n > total_count:
        print(
            f"Warning: requested {n} files but only {total_count} available, using all"
        )
        n = total_count

    sampled = random.sample(all_files, n)
    print(f"Sampled {n} of {total_count} files from {directory}")

    script_path = Path(__file__).resolve().parent / "upload_to_knowledge.py"

    with tempfile.TemporaryDirectory(prefix="benchmark_upload_") as tmpdir:
        for f in sampled:
            shutil.copy2(f, tmpdir)

        knowledge_name = f"_benchmark_{directory.name}_{n}"
        cmd = [
            sys.executable,
            str(script_path),
            tmpdir,
            "--api-key",
            args.api_key,
            "--knowledge-name",
            knowledge_name,
            "--base-url",
            args.base_url,
        ]

        print(f"\nUploading {n} files to temporary knowledge base '{knowledge_name}'...")
        start = time.monotonic()
        result = subprocess.run(cmd)
        elapsed = time.monotonic() - start

        if result.returncode != 0:
            print(f"\nUpload failed (exit code {result.returncode})")
            sys.exit(1)

    per_file = elapsed / n
    estimated_total = per_file * total_count

    # Clean up the temporary knowledge base
    print(f"\nCleaning up temporary knowledge base '{knowledge_name}'...")
    headers = {
        "Authorization": f"Bearer {args.api_key}",
        "Accept": "application/json",
    }
    try:
        with httpx.Client(base_url=args.base_url, timeout=120) as client:
            resp = client.get("/api/v1/knowledge/", headers=headers)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("items", data) if isinstance(data, dict) else data
            for kb in items:
                if kb["name"] == knowledge_name:
                    resp = client.delete(
                        f"/api/v1/knowledge/{kb['id']}/delete",
                        headers=headers,
                    )
                    resp.raise_for_status()
                    print(f"Deleted knowledge base '{knowledge_name}'")
                    break
            else:
                print(f"Warning: could not find knowledge base '{knowledge_name}' to delete")
    except Exception as e:
        print(f"Warning: failed to delete knowledge base: {e}")

    print(f"\n{'=' * 50}")
    print(f"Benchmark results")
    print(f"{'=' * 50}")
    print(f"Files sampled:       {n} / {total_count}")
    print(f"Time elapsed:        {elapsed:.1f}s")
    print(f"Time per file:       {per_file:.2f}s")
    print(f"Estimated total:     {estimated_total:.1f}s ({estimated_total / 60:.1f} min) for all {total_count} files")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
