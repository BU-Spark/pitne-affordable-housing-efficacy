import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import argparse
from pathlib import Path
from tools.google_drive import (
    get_drive_service,
    get_or_choose_dataset_folder_id,
    list_files_in_folder,
    download_file,
)


def main():
    p = argparse.ArgumentParser(description="Download a file from the 'Dataset' Drive folder.")
    p.add_argument("--name", required=True, help="Exact filename (e.g., applications_2025.csv)")
    p.add_argument("--out", default="data", help="Local output dir (default: data/)")
    args = p.parse_args()


    svc = get_drive_service()
    folder_id = get_or_choose_dataset_folder_id(svc, name="Dataset")
    files = list_files_in_folder(svc, folder_id)


    matches = [f for f in files if f["name"] == args.name]
    if not matches:
        print(f"No file named '{args.name}' in the Dataset folder.")
        return
    if len(matches) > 1:
        print(f"Warning: multiple files named '{args.name}'. Downloading the first.")


    file = matches[0]
    out_path = Path(args.out) / file["name"]
    download_file(svc, file_id=file["id"], local_path=out_path)
    print(f"✅ Downloaded to {out_path}")


if __name__ == "__main__":
    main()