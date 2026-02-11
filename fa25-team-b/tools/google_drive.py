from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Smallest scope that lets us read files
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

ROOT = Path(__file__).resolve().parents[1]
SECRETS = ROOT / "secrets"
CLIENT_FILE = SECRETS / "oauth_client.json"
TOKEN_FILE = SECRETS / "token.json"
CACHE = SECRETS / ".drive_cache.json"


# Toggle these to True if your 'Dataset' lives in a Shared Drive (Team Drive)
USE_SHARED_DRIVE = False # set to True if needed

def resolve_target_folder_id(service, possible_id: str) -> str:
    """
    If given a shortcut, follow it to the real target folder id.
    Otherwise return the id unchanged. Works for Shared Drives too.
    """
    meta = service.files().get(
        fileId=possible_id,
        fields="id, mimeType, shortcutDetails",
        supportsAllDrives=True
    ).execute()

    mt = meta.get("mimeType", "")
    if mt == "application/vnd.google-apps.shortcut":
        target_id = meta.get("shortcutDetails", {}).get("targetId")
        if not target_id:
            raise RuntimeError("Shortcut has no targetId.")
        # Confirm target is a folder (optional but helpful)
        tmeta = service.files().get(
            fileId=target_id,
            fields="id, mimeType, name",
            supportsAllDrives=True
        ).execute()
        if tmeta.get("mimeType") != "application/vnd.google-apps.folder":
            raise RuntimeError(f"Shortcut target is not a folder: {tmeta}")
        return target_id
    elif mt == "application/vnd.google-apps.folder":
        return possible_id
    else:
        raise RuntimeError(f"Provided id is not a folder or shortcut to a folder: mimeType={mt}")

def _load_cache() -> dict:
    if CACHE.exists():
        return json.loads(CACHE.read_text())
    return {}

def _save_cache(obj: dict) -> None:
    SECRETS.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(obj, indent=2))

def get_drive_service():
    """Authenticate the user (first run opens a browser) and return a Drive API client."""
    SECRETS.mkdir(parents=True, exist_ok=True)


    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return build("drive", "v3", credentials=creds)

def get_or_choose_dataset_folder_id(service, name: str = "Dataset") -> str:
    """
    Resolve the Dataset folder ID, in this order:
      1) repo-root DATASET_FOLDER_ID file (committed, preferred)
      2) DATASET_FOLDER_ID environment variable
      3) cached id in secrets/.drive_cache.json
      4) fallback: search by name (your drive, shared-with-me, etc.)
    """
    import os
    from pathlib import Path

    # 1) Repo-root file
    root_id_file = Path(__file__).resolve().parents[1] / "DATASET_FOLDER_ID"
    if root_id_file.exists():
        raw_id = root_id_file.read_text().strip()
        if raw_id:
            rid = resolve_target_folder_id(service, raw_id)
            cache = _load_cache()
            cache["dataset_folder_id"] = rid
            _save_cache(cache)
            return rid


    # 2) Env var
    env_id = os.getenv("DATASET_FOLDER_ID")
    if env_id:
        rid = resolve_target_folder_id(service, env_id)
        cache = _load_cache()
        cache["dataset_folder_id"] = rid
        _save_cache(cache)
        return rid


    # 3) Cached
    cache = _load_cache()
    if cache.get("dataset_folder_id"):
        return cache["dataset_folder_id"]

    # 4) Fallback search (can be flaky for shared-with-me, but we’ll try)
    def _list(q: str):
        kwargs = {
            "q": q,
            "fields": "files(id, name, owners(displayName), parents)",
            "pageSize": 1000,
        }
        if USE_SHARED_DRIVE:
            kwargs.update({
                "supportsAllDrives": True,
                "includeItemsFromAllDrives": True,
            })
        return service.files().list(**kwargs).execute().get("files", [])

    q1 = "name = '{n}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false".format(n=name)
    hits = _list(q1)

    if not hits:
        q2 = ("name = '{n}' and mimeType = 'application/vnd.google-apps.folder' "
              "and trashed = false and sharedWithMe = true").format(n=name)
        hits = _list(q2)

    if not hits:
        q3 = ("name contains '{n}' and mimeType = 'application/vnd.google-apps.folder' "
              "and trashed = false").format(n=name)
        hits = _list(q3)

    if not hits:
        raise RuntimeError(f"No folder named '{name}' visible to this account (including shared-with-me). "
                           "Add DATASET_FOLDER_ID at repo root to skip search.")

    if len(hits) == 1:
        folder_id = hits[0]["id"]
        cache["dataset_folder_id"] = folder_id
        _save_cache(cache)
        return folder_id

    print("Multiple candidate folders found:")
    for i, f in enumerate(hits, 1):
        owner = f.get("owners", [{}])[0].get("displayName", "?")
        print(f"[{i}] {f['name']}  id={f['id']}  owner={owner}")
    choice = int(input("Choose the number: "))
    folder_id = hits[choice - 1]["id"]
    cache["dataset_folder_id"] = folder_id
    _save_cache(cache)
    return folder_id




def list_files_in_folder(service, folder_id: str) -> List[Dict]:
    folder_id = resolve_target_folder_id(service, folder_id)  # safety if someone passes a shortcut
    q = f"'{folder_id}' in parents and trashed = false"
    files, page_token = [], None

    kwargs = {
        "q": q,
        "spaces": "drive",
        "fields": "nextPageToken, files(id, name, mimeType, modifiedTime, size)",
        "pageSize": 1000,
        "supportsAllDrives": True,
        "includeItemsFromAllDrives": True,
        "corpora": "allDrives",
    }

    while True:
        resp = service.files().list(pageToken=page_token, **kwargs).execute()
        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return files

def download_file(service, file_id: str, local_path: Path) -> Path:
    from googleapiclient.http import MediaIoBaseDownload
    import io


    local_path.parent.mkdir(parents=True, exist_ok=True)


    kwargs = {"fileId": file_id}
    if USE_SHARED_DRIVE:
        kwargs["supportsAllDrives"] = True


    request = service.files().get_media(**kwargs)
    fh = io.FileIO(local_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return local_path