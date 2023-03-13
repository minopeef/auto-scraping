import json
import re
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


class Base:
    def __init__(self) -> None:
        self.name = None
        self.path = None
        self.url = None
        self.driver_id = None

    def download_img(self, path: str, driver_id: str, link: str, name: str):
        r = requests.get(link, stream=True)
        r.raw.decode_content = True
        with open(f"{path}/{name}", "wb") as f:
            shutil.copyfileobj(r.raw, f)
        self.upload_file(driver_id, f"{path}/{name}")

    def save_upload_audio(self, local_path: str, driver_id: str, text: str):
        api_url = "https://www.yukumo.net/api/v2/aqtk1/koe.mp3"
        if len(text) > 140:
            text = text[:140]
        params = {
            "type": "f1",
            "effect": "none",
            "boyomi": "true",
            "speed": "150",
            "volume": "100",
            "kanji": text,
        }
        # headers = {
        #     "user-agent": """user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
        #     (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"""
        # }
        resp = requests.get(url=api_url, params=params)
        with open(local_path, "wb") as f:
            f.write(resp.content)
        self.upload_file(driver_id, local_path)
        return

    def save_upload_txt(self, local_path: str, driver_id: str, txt: str):
        with open(local_path, mode="w", encoding="utf-8") as f:
            f.write(txt)
        self.upload_file(driver_id, local_path)
        return

    def create_driver_directory(self, directory_name: str, parent_id="root"):
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

    def upload_file(self, driver_id: str, local_path: str):
        file_name = local_path.split("/")[-1]
        file = drive.CreateFile({"title": file_name, "parents": [{"id": driver_id}]})
        file.SetContentFile(local_path)
        file.Upload()
        return file["id"]

    def run():
        pass

    def save_upload(self):
        # create local path
        Path(f"{self.article_path}/音声ファイル").mkdir(parents=True, exist_ok=True)
        Path(f"{self.article_path}/記事").mkdir(parents=True, exist_ok=True)

        # create driver path
        self.article_driver_id = self.create_driver_directory(
            f"{self.date_time}_{self.article_head}", self.driver_id
        )
        self.audio_driver_id = self.create_driver_directory(
            "音声ファイル", self.article_driver_id
        )
        self.comment_driver_id = self.create_driver_directory(
            "記事", self.article_driver_id
        )

        # save image
        [
            self.download_img(
                self.article_path, self.article_driver_id, x, f"{idx}_img.jpg"
            )
            for idx, x in enumerate(self.img_link)
        ]

        # download audio and comment
        for idx, item in enumerate(self.comment_body_list):
            try:
                # temp_arr = re.findall(r"\w+", item)
                # file_name = str(idx) + "_" + temp_arr[1] + temp_arr[-1]
                file_name = item
                if len(item) > 5:
                    file_name = item[:5]

                if idx < 10:
                    file_name = f"0{idx}_{file_name}"
                else:
                    file_name = f"{idx}_{file_name}"

                self.save_upload_audio(
                    f"{self.article_path}/音声ファイル/{file_name}.mp3",
                    self.audio_driver_id,
                    item,
                )

                self.save_upload_txt(
                    f"{self.article_path}/記事/{file_name}.txt",
                    self.comment_driver_id,
                    item,
                )
            except:  # noqa
                continue
        with open(
            f"{self.article_path}/all_info.json", mode="w", encoding="utf-8"
        ) as f:
            json.dump(self.result, f, ensure_ascii=False)
        self.upload_file(self.article_driver_id, f"{self.article_path}/all_info.json")


# なんJ PRIDE
class Rock(Base):
    def __init__(self) -> None:
        self.name = "なんJ PRIDE"
        self.path = "自動化/なんJ PRIDE"
        self.url = "http://blog.livedoor.jp/rock1963roll/"
        self.driver_id = "1DVSgFkkssr7dBehXeMkE8nwdfi4say8u"
        self.result = []

    def run(self):
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.text, features="html.parser")
        recent_tag = soup.find("ul", attrs={"class": "recent-article-image"})
        recent_link_list = [x.find("a")["href"] for x in recent_tag.find_all("li")]
        for _link in recent_link_list:
            result = {
                "title": "",
                "link": _link,
                "path": "",
                "comment": [],
                "img_link": [],
            }
            # get all html
            resp = requests.get(_link)
            soup = BeautifulSoup(resp.text, features="html.parser")

            # get article head html
            self.article_head = soup.find("div", attrs={"class": "article-header"})

            # get deployed time
            self.date_time = self.article_head.find("abbr")["title"]
            self.date_time = "".join(re.findall(r"\d+", self.date_time))[:12]

            # get title
            title = self.article_head.find("h2").text.strip()
            result["title"] = title

            # get save path
            self.article_head = " ".join(re.findall(r"\w+", title)).strip()
            self.article_path = f"{self.path}/{self.date_time}_{self.article_head}"
            result["path"] = self.article_path

            # get article body html
            article_body = soup.find("div", attrs={"class": "article-body-inner"})

            # get image link
            self.img_link = [x["src"] for x in article_body.find_all("img")]
            result["img_link"] = self.img_link

            # get comment head and body
            self.comment_head_list = [
                x.text.strip()
                for x in article_body.find_all("div", attrs={"class": "t_h"})
            ]
            self.comment_body_list = [
                x.text.strip()
                for x in article_body.find_all("div", attrs={"class": "t_b"})
            ]
            result["comment"] = self.comment_body_list
            self.result.append(result)
            self.save_upload()
        return


class Yakiusoku(Base):
    def __init__(self) -> None:
        self.name = "日刊やきう速報"
        self.path = "自動化/日刊やきう速報"
        self.url = "http://blog.livedoor.jp/yakiusoku/"
        self.driver_id = "1oFjp2Mg_AlCOLeEpCIFZT3zibdtinlNE"
        self.result = []

    def run(self):
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.text, features="html.parser")
        recent_tag = soup.find("ul", attrs={"class": "recent-article-image"})
        recent_link_list = [x.find("a")["href"] for x in recent_tag.find_all("li")]
        for _link in recent_link_list:
            result = {
                "title": "",
                "link": _link,
                "path": "",
                "comment": [],
                "img_link": [],
            }
            # get all html
            resp = requests.get(_link)
            soup = BeautifulSoup(resp.text, features="html.parser")

            # get article head html
            self.article_head = soup.find(attrs={"class": "article-header"})

            # get deployed time
            self.date_time = self.article_head.find(
                attrs={"class": "article-date"}
            ).text.strip()
            self.date_time = "".join(re.findall(r"\d+", self.date_time))[:12]

            # get title
            title = self.article_head.find(
                attrs={"class": "article-title"}
            ).text.strip()
            result["title"] = title

            # get save path
            self.article_head = " ".join(re.findall(r"\w+", title)).strip()
            self.article_path = f"{self.path}/{self.date_time}_{self.article_head}"
            result["path"] = self.article_path

            # get article body html
            article_body = soup.find("div", attrs={"class": "article-body-inner"})

            # get image link
            self.img_link = [x["src"] for x in article_body.find_all("img")]
            result["img_link"] = self.img_link

            # get comment head and body
            # self.comment_head_list = [
            #     x.text.strip()
            #     for x in article_body.find_all("div", attrs={"class": "t_h"})
            # ]
            self.comment_body_list = [
                x.text.strip()
                for x in article_body.find_all("div", attrs={"class": "t_b"})
            ]
            result["comment"] = self.comment_body_list
            self.result.append(result)
            self.save_upload()
        return


class Livejupiter2(Base):
    def __init__(self) -> None:
        self.name = "なんJ（まとめては）いかんのか？"
        self.path = "自動化/なんJ（まとめては）いかんのか？"
        self.url = "http://blog.livedoor.jp/livejupiter2/"
        self.driver_id = "1GJxSjcyk6qB27kpXjBuysM27AjiT9HLk"
        self.result = []

    def run(self):
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.text, features="html.parser")
        recent_tag = soup.find("ul", attrs={"class": "recent-article-image"})
        recent_link_list = [x.find("a")["href"] for x in recent_tag.find_all("li")]
        for _link in recent_link_list:
            result = {
                "title": "",
                "link": _link,
                "path": "",
                "comment": [],
                "img_link": [],
            }
            # get all html
            resp = requests.get(_link)
            soup = BeautifulSoup(resp.text, features="html.parser")

            # get article head html
            self.article_head = soup.find(attrs={"class": "article-header"})

            # get title
            title = self.article_head.find(
                attrs={"class": "article-title"}
            ).text.strip()
            result["title"] = title

            # get article body html
            article_body = soup.find(
                "div", attrs={"class": "article-body entry-content"}
            )

            # get deployed time
            self.date_time = article_body.find("abbr")["title"].strip()
            self.date_time = "".join(re.findall(r"\d+", self.date_time))[:12]

            # get save path
            self.article_head = " ".join(re.findall(r"\w+", title)).strip()
            self.article_path = f"{self.path}/{self.date_time}_{self.article_head}"
            result["path"] = self.article_path

            # get image link
            self.img_link = [x["src"] for x in article_body.find_all("img")]
            result["img_link"] = self.img_link
            self.comment_body_list = []
            # get comment head and body
            for item in article_body.find_all("dd"):
                try:
                    self.comment_body_list.append(
                        " ".join(re.findall(r"\w+", item.find("b").text.strip()))
                    )
                except:  # noqa
                    continue

            result["comment"] = self.comment_body_list
            self.result.append(result)
            self.save_upload()


# Rock().run()
# Yakiusoku().run()
Livejupiter2().run()
# Base().download_audio("static","""abc""")
# print(os.listdir("自動化/MLB NEWS@まとめ"))
