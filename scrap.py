import json
import re
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class Base:
    def __init__(self) -> None:
        self.name = None
        self.path = None
        self.url = None

    def download_img(self, path: str, link: str):
        r = requests.get(link, stream=True)
        r.raw.decode_content = True
        with open(f"{path}/img.png", "wb") as f:
            shutil.copyfileobj(r.raw, f)

    def save_audio(self, path: str, text: str):
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
        headers = {
            "user-agent": """user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
            (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"""
        }
        resp = requests.get(url=api_url, params=params, headers=headers)
        with open(path, "wb") as f:
            f.write(resp.content)

    # def save_info_local(self, title, path, comment: str, img_link: str):
    #     # crete directory
    #     audio_path = f"{path}/音声ファイル"
    #     Path(audio_path).mkdir(parents=True, exist_ok=True)

    #     # save comment as txt
    #     with open(f"{path}/comment.txt", mode="w", encoding="utf-8") as f:
    #         f.write(comment)

    #     # save img
    #     self.download_img(path, img_link)

    #     # save comment as audio
    #     self.download_audio(audio_path, comment)

    def save_txt(self, path, txt):
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(txt)

    def run():
        pass


# なんJ PRIDE
class Whatjpride(Base):
    def __init__(self) -> None:
        self.name = "なんJ PRIDE"
        self.path = "自動化/なんJ PRIDE"
        self.url = "http://blog.livedoor.jp/rock1963roll/"

    def run(self):
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.text, features="html.parser")
        ul_tag = soup.find("ul", attrs={"class": "recent-article-image"})
        link_list = [x.find("a")["href"] for x in ul_tag.find_all("li")]
        for _link in link_list:
            result = {
                "title": "",
                "link": _link,
                "path": "",
                "comment": [],
                "img_link": "",
            }
            # get all html
            resp = requests.get(_link)
            soup = BeautifulSoup(resp.text, features="html.parser")

            # get article head html
            article_head = soup.find("div", attrs={"class": "article-header"})

            # get deployed time
            date_time = article_head.find("abbr")["title"]
            date_time = "".join(re.findall(r"\d+", date_time))[:12]

            # get title
            title = article_head.find("h2").text.strip()
            result["title"] = title

            # get save path
            article_head = " ".join(re.findall(r"\w*", title)).strip()
            path = f"{self.path}/{date_time}_{article_head}"
            result["path"] = path

            # get article body html
            article_body = soup.find("div", attrs={"class": "article-body-inner"})

            # get image link
            img_link = article_body.find_all("img")[0]["src"]
            result["img_link"] = img_link

            # create path
            Path(f"{path}/音声ファイル").mkdir(parents=True, exist_ok=True)

            # save image
            self.download_img(path, img_link)

            # get comment head and body
            comment_head_list = [
                x.text.strip()
                for x in article_body.find_all("div", attrs={"class": "t_h"})
            ]
            comment_body_list = [
                x.text.strip()
                for x in article_body.find_all("div", attrs={"class": "t_b"})
            ]

            # download audio and comment
            for idx, item in comment_head_list:
                result["comment"].append({"head": item, "body": comment_body_list[idx]})
                file_name = str(idx) + "_" + " ".join(re.findall(r"\w*", item))

                self.save_audio(
                    f"{path}/音声ファイル/{file_name}.mp3", comment_body_list[idx]
                )

                self.save_txt(f"{path}/{file_name}.txt", comment_body_list[idx])
            with open("all_info.json", mode="w", encoding="utf-8") as f:
                f.write(json.dumps(result))

        return


Whatjpride().run()
# Base().download_audio("static","""abc""")
# print(os.listdir("自動化/MLB NEWS@まとめ"))
