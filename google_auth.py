"""Loads the Google OAuth token from the private folder (GOOGLE_PRIVATE_DIR).

The secrets are NEVER copied into this project. The server never opens a browser:
if the token is missing or cannot be refreshed, it raises a clear error instead.
"""
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
]


def private_dir() -> Path:
    value = os.environ.get("GOOGLE_PRIVATE_DIR")
    if not value:
        raise RuntimeError("GOOGLE_PRIVATE_DIR is not set (it must point to the private folder).")
    folder = Path(value)
    if not folder.is_dir():
        raise RuntimeError("GOOGLE_PRIVATE_DIR must point to a folder, not a file.")
    return folder


def get_credentials() -> Credentials:
    token_file = private_dir() / "token.json"
    if not token_file.exists():
        raise RuntimeError("token.json not found. Run last week's L05/LO6 program once to create it.")
    creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    if creds.valid:
        return creds
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_file.write_text(creds.to_json(), encoding="utf-8")  # same private folder
        return creds
    raise RuntimeError("token.json is invalid. Delete it and run the L05/LO6 program again.")


_services: dict = {}


def service(name: str, version: str):
    """Cached Google API client (gmail v1 / calendar v3)."""
    key = f"{name}:{version}"
    if key not in _services:
        _services[key] = build(name, version, credentials=get_credentials(), cache_discovery=False)
    return _services[key]
