from pathlib import Path

import pandas
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("credentials")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("credentials")
drive = GoogleDrive(gauth)


root_name = "自動化"
sites = [
    "なんJ PRIDE",
    "なんJ（まとめては）いかんのか？",
    "なんじぇいスタジアム＠なんJまとめ",
    "MLB NEWS@まとめ",
    "日刊やきう速報",
]


def create_driver_directory(directory_name: str, parent_id="root"):
    file_metadata = {
        "title": directory_name,
        # "parents": [{"id": parent_id}],
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id != "root":
        file_metadata["parents"] = [{"id": parent_id}]
    folder = drive.CreateFile(file_metadata)
    folder.Upload()
    return folder["id"]


# create local path

root_id = create_driver_directory(root_name)
result = {"name": [], "id": []}
for x in sites:
    Path(f"{root_name}/{x}").mkdir(parents=True, exist_ok=True)
    id = create_driver_directory(x, root_id)
    result["id"].append(id)
    result["name"].append(x)
df = pandas.DataFrame(result)
df.to_csv("drive_info.csv", mode="w", header=True, index=False, encoding="utf-8")
