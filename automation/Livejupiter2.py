import re

import pandas
import requests
from bs4 import BeautifulSoup

from automation.Base import Base


class Livejupiter2(Base):
    def __init__(self) -> None:
        self.name = "なんJ（まとめては）いかんのか？"
        self.path = "自動化/なんJ（まとめては）いかんのか？"
        self.url = "http://blog.livedoor.jp/livejupiter2/"
        self.result = []
        df = pandas.read_csv("drive_info.csv")
        self.driver_id = df[df["name"] == self.name]["id"][0]
        # self.driver_id = "1GJxSjcyk6qB27kpXjBuysM27AjiT9HLk"

    def run(self):
        print("scraping なんJ（まとめては）いかんのか？")
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.text, features="html.parser")
        recent_tag = soup.find("ul", attrs={"class": "recent-article-image"})
        recent_link_list = [x.find("a")["href"] for x in recent_tag.find_all("li")][:1]
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
            self.run_premiere()
