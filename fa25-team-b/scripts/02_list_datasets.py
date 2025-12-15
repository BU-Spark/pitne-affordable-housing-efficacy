import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.google_drive import (
    get_drive_service,
    get_or_choose_dataset_folder_id,
    list_files_in_folder,
)


if __name__ == "__main__":
    svc = get_drive_service()
    folder_id = get_or_choose_dataset_folder_id(svc, name="Dataset")
    print(f"Using Dataset folder id: {folder_id}")
    files = list_files_in_folder(svc, folder_id)
if not files:
    print("No files found.")
else:
    for f in files:
        size = f.get("size", "?")
        print(f"{f['name']} | {f['mimeType']} | {size} bytes | id={f['id']}")