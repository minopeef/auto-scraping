import os
import time
from datetime import datetime

from dotenv import load_dotenv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
load_dotenv()
root_id = os.getenv("ROOT_ID")
unprocess_id = None
process_id = None


def create_directory():
    global unprocess_id
    global process_id
    ts = int(time.time())
    folder_name = str(datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"))

    file_metadata = {
        "title": folder_name,
        "parents": [{"id": root_id}],
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = drive.CreateFile(file_metadata)
    folder.Upload()
    parent_id = folder["id"]

    file_metadata = {
        "title": "unprocess",
        "parents": [{"id": parent_id}],
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = drive.CreateFile(file_metadata)
    folder.Upload()
    unprocess_id = folder["id"]

    file_metadata["title"] = "process"
    folder = drive.CreateFile(file_metadata)
    folder.Upload()
    process_id = folder["id"]


# upload file to a directory that id is @_folder
# def upload_drive():
#     file1 = drive.CreateFile({"title": "Hello.jpg", 'parents': [{'id': current_folder_id}]})
#     file1.SetContentFile("app.py")
#     file1.Upload()


# def download_drive(_folder = folder_id):
#     file_list = get_file_list()
#     for i, file1 in enumerate(sorted(file_list, key = lambda x: x['title']), start=1):
#         print('Downloading {} from GDrive ({}/{})'.format(file1['title'], i, len(file_list)))
#         file1.GetContentFile(file1['title'])


# def get_file_list(_folder = folder_id):
# 	file_list = drive.ListFile({'q': f"'{_folder}' in parents and trashed=false"}).GetList()
# 	return file_list

create_directory()
print(unprocess_id, process_id)
# upload_drive()

# Create the folder
# If no parent ID is provided this will automatically go to the root or My Drive 'directory'
# top_level_folder = drive.CreateFile({'title': 'top_level', 'mimeType': 'application/vnd.google-apps.folder'})
# # Upload the file to your drive
# top_level_folder.Upload()
# # Grab the ID of the folder we just created
# parent_id = top_level_folder['id']
# print(parent_id)
# # Create a sub-directory
# # Make sure to assign it the proper parent ID
# child_folder = drive.CreateFile({'title': 'level_2', 'parents':[{'id':parent_id}], 'mimeType': 'application/vnd.google-apps.folder'})
# child_folder.Upload()
