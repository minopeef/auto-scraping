import json
import re
import shutil
import time
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

    def download_audio(self, path, text):
        api_url = "https://large-text-to-speech.p.rapidapi.com/tts"

        payload = {"text": text}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "9929ce4c9dmsh8310848ee5c940cp1da3f8jsnf3c41c1289ad",
            "X-RapidAPI-Host": "large-text-to-speech.p.rapidapi.com",
        }

        response = requests.request("POST", api_url, json=payload, headers=headers)
        # filename = "test-file.wav"
        id = json.loads(response.text)["id"]
        eta = json.loads(response.text)["eta"]
        print(f"Waiting {eta} seconds for the job to finish...")
        time.sleep(eta)
        response = requests.request("GET", api_url, headers=headers, params={"id": id})
        while "url" not in json.loads(response.text):
            response = requests.request(
                "GET", api_url, headers=headers, params={"id": id}
            )
            print(f"Waiting some more...")
            time.sleep(3)
        api_url = json.loads(response.text)["url"]
        response = requests.request("GET", api_url)
        with open(f"{path}/audio.wav", "wb") as f:
            f.write(response.content)

    def save_info_local(self, title, path, comment: str, img_link: str):
        # crete directory
        audio_path = f"{path}/音声ファイル"
        Path(audio_path).mkdir(parents=True, exist_ok=True)

        # save comment as txt
        with open(f"{path}/comment.txt", mode="w", encoding="utf-8") as f:
            f.write(comment)

        # save img
        self.download_img(path, img_link)

        # save comment as audio
        self.download_audio(audio_path, comment)

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
        # result = {}
        for link in link_list:
            resp = requests.get(link)
            soup = BeautifulSoup(resp.text, features="html.parser")
            article_head = soup.find("div", attrs={"class": "article-header"})

            date_time = article_head.find("abbr")["title"]
            date_time = "".join(re.findall(r"\d+", date_time))[:12]

            title = article_head.find("h2").text.strip()
            article_head = " ".join(re.findall(r"\w*", title)).strip()
            path = f"{self.path}/{date_time}_{article_head}"
            # audio_path = f"{date_time}_{article_head}/音声ファイル"
            article_body = soup.find("div", attrs={"class": "article-body-inner"})
            img_link = article_body.find_all("img")[0]["src"]

            # result["comment_head_list"] = [x.text.strip() for x in article_body.find_all("div", attrs={"class": "t_h"})]
            # result["comment_body_list"] = [x.text.strip() for x in article_body.find_all("div", attrs={"class": "t_b"})]
            comment = "\n".join(
                [
                    x.text.strip()
                    for x in article_body.find_all("div", attrs={"class": "t_b"})
                ]
            )

            self.save_info_local(
                title=title, path=path, comment=comment, img_link=img_link
            )
        return


Whatjpride().run()
# Base().download_audio(1,2)
# print(os.listdir("自動化/MLB NEWS@まとめ"))
