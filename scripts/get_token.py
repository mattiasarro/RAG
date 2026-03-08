# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx",
# ]
# ///
"""Get a JWT token from Open WebUI by signing in with email and password.

Usage:
    uv run scripts/get_token.py --email user@example.com --password secret
    uv run scripts/get_token.py --email user@example.com  # prompts for password

Use the token with upload_to_knowledge.py:
    uv run scripts/upload_to_knowledge.py data/et_wiki_100 \\
        --api-key $(uv run scripts/get_token.py --email user@example.com --password secret)
"""

import argparse
import getpass
import sys

import httpx

DEFAULT_BASE_URL = "http://localhost:3000"


def main():
    parser = argparse.ArgumentParser(description="Get Open WebUI JWT token")
    parser.add_argument("--email", required=True, help="Open WebUI email")
    parser.add_argument("--password", default=None, help="Open WebUI password (prompts if omitted)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"Open WebUI base URL (default: {DEFAULT_BASE_URL})")
    args = parser.parse_args()

    password = args.password or getpass.getpass("Password: ")

    resp = httpx.post(
        f"{args.base_url}/api/v1/auths/signin",
        json={"email": args.email, "password": password},
    )
    if resp.status_code != 200:
        print(f"Error: {resp.status_code} {resp.text}", file=sys.stderr)
        sys.exit(1)

    print(resp.json()["token"])


if __name__ == "__main__":
    main()
