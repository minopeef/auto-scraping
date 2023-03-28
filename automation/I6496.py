import re

import pandas
import requests
from bs4 import BeautifulSoup

from automation.Base import Base


# なんJ PRIDE
class I6496(Base):
    def __init__(self) -> None:
        self.name = "MLB NEWS@まとめ"
        self.path = "自動化/MLB NEWS@まとめ"
        self.url = "http://blog.livedoor.jp/i6469/"
        self.result = []
        df = pandas.read_csv("drive_info.csv")
        self.driver_id = df[df["name"] == self.name]["id"].iloc[0]

    def run(self):
        print(f"scraping {self.name}")
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.text, features="html.parser")
        recent_tag = soup.find("div", attrs={"class": "plugin-recent_articles"})
        recent_link_list = [
            x.find("a")["href"]
            for x in recent_tag.find_all(attrs={"class": "sidebody"})
        ][:10]
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

            # check if it is new article
            if not self.check_interval(self.date_time):
                continue

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
            self.run_premiere()
        return
