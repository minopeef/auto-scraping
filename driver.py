import os
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# load_dotenv()
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
# drive = GoogleDrive(gauth)

# root_folder = os.getenv("ROOT_FOLDER")
# root_id = "1NhePmlSL9o6J4_2iO59KuQ8O0BGjMObk" # 自動化

# MLB_NEWS_Summary = "1WVO-MNUrlt4sw-mhJf3OIEMy1Uyy9VNP" # MLB NEWS@まとめ
# What_J_PRIDE = "1uOXxuaaQA4dgX8puRF49-Mbzdb21Eonp" # なんJ PRIDE
# How_is_it = "1b8Kco3Usi_kPGv85x7--5GjUIjf7bhRm"  # なんJ（まとめては）いかんのか？
# Nanjiei_Stadium_NJ_Summary = "1b8Kco3Usi_kPGv85x7--5GjUIjf7bhRm" # なんじぇいスタジアム＠なんJまとめ
# Daily_Yakitori_Bulletin = "1PeobqCDOWgZ_dLrAtIDLR2GqES3gvEk7" # 日刊やきう速報


# def create_directory(name, parent_id="root"):
#     file_metadata = {
#         "title": name,
#         # "parents": [{"id": parent_id}],
#         "mimeType": "application/vnd.google-apps.folder",
#     }
#     if parent_id != "root":
#         file_metadata["parents"] = [{"id": parent_id}]
#     folder = drive.CreateFile(file_metadata)
#     folder.Upload()

# def get_file_list(directory_id):
#     pass

# def get_folder_list(directory_id = "root"):
#     folder_list = drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
#     print([x["title"] for x in folder_list])
#     # file_list = drive.ListFile({'q': "'<folder ID>' in parents and trashed=false"}).GetList()
#     # pass
# get_folder_list()


# def init_directory():
#     pass


# root_folder_flag = [x for x in folder_list if x["title"] == root_folder]
# if root_folder_flag:
#     root_id = root_folder_flag[0]
# else:
#     file_metadata = {
#         "title": root_folder,
#         "mimeType": "application/vnd.google-apps.folder",
#     }
#     folder = drive.CreateFile(file_metadata)
#     folder.Upload()
#     root_id = folder["id"]

# def create_directory():
#     global unprocess_id
#     global process_id
#     ts = int(time.time())
#     folder_name = str(datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"))

#     file_metadata = {
#         "title": folder_name,
#         "parents": [{"id": root_id}],
#         "mimeType": "application/vnd.google-apps.folder",
#     }
#     folder = drive.CreateFile(file_metadata)
#     folder.Upload()
#     parent_id = folder["id"]

#     file_metadata = {
#         "title": "unprocess",
#         "parents": [{"id": parent_id}],
#         "mimeType": "application/vnd.google-apps.folder",
#     }
#     folder = drive.CreateFile(file_metadata)
#     folder.Upload()
#     unprocess_id = folder["id"]

#     file_metadata["title"] = "process"
#     folder = drive.CreateFile(file_metadata)
#     folder.Upload()
#     process_id = folder["id"]


# # upload file to a directory that id is @_folder
# def upload_files(folder_id):
#     file1 = drive.CreateFile({"title": "Hello.jpg", 'parents': [{'id': folder_id}]})
#     file1.SetContentFile("app.py")
#     file1.Upload()


# def scrap():
#     pass


# create_directory()
# print(unprocess_id, process_id)

# # scraping & save files to local

# upload_files(unprocess_id)

# # allow files into premiere

# # process files to video manually

# upload_files(process_id)


# # restart
