from __future__ import annotations
from pathlib import Path
import argparse, yaml
from tools.google_drive import get_drive_service, get_or_choose_dataset_folder_id, download_file


RAW_DIR = Path("data/raw")
CONFIG = Path("config/datasets.yaml")




def export_google_sheet_to_csv(service, file_id: str, out_path: Path):
    from googleapiclient.http import MediaIoBaseDownload
    import io
    request = service.files().export(fileId=file_id, mimeType="text/csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fh = io.FileIO(out_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return out_path




def main(kind: str | None):
    service = get_drive_service()
    folder_id = get_or_choose_dataset_folder_id(service, name="Dataset")


    cfg = yaml.safe_load(CONFIG.read_text())
    targets = []
    if kind is None or kind == "applications":
        targets.extend(cfg.get("applications", []))
    if kind is None or kind == "resales":
        targets.extend(cfg.get("resales", []))


    excludes = set(cfg.get("excludes", []))


    RAW_DIR.mkdir(parents=True, exist_ok=True)


    for t in targets:
        name = t["name"]
        fid = t["id"]
        ftype = t.get("type", "xlsx")
        if name in excludes:
            continue
        out_name = name.replace(" ", "_").replace("/", "-")
        out = RAW_DIR / (out_name + (".csv" if ftype == "google_sheet" else ""))
        print(f"Pulling {name} → {out}")
        if ftype == "google_sheet":
            export_google_sheet_to_csv(service, fid, out)
        else:
            download_file(service, fid, out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Pull datasets from Drive to data/raw/")
    ap.add_argument("--kind", choices=["applications", "resales"], default=None)
    args = ap.parse_args()
    main(args.kind)