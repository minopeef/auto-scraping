import datetime
import json
import os
import re
import shutil
import time
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import pymiere
import requests
from matplotlib import font_manager
from matplotlib.figure import Figure
from mutagen.mp3 import MP3
from PIL import Image
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pymiere.wrappers import time_from_seconds

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

# add font to matplotlib
font_manager.fontManager.addfont("gen.ttf")


class Base:
    all_comment = ""
    interval = 20  # 分
    line_width = 20  # 文字数
    line_height = 10  # 行数
    comment_body_list = []
    font_size = 20

    def __init__(self) -> None:
        self.name = None
        self.path = None
        self.url = None
        self.driver_id = None
        self.article_path = None
        self.date_time = None
        self.article_head = None
        self.img_link = None
        self.result_movie_path = None

    def check_interval(self, _time):

        cur_time = int(time.time())

        try:
            dt = datetime.datetime.fromisoformat(_time)
        except:  # noqa
            temp = re.findall(r"\d+", _time)[:5]
            temp = f"{temp[0]}-{temp[1]}-{temp[2]}T{temp[3]}:{temp[4]}:00+09:00"
            dt = datetime.datetime.fromisoformat(temp)

        if cur_time - dt.timestamp() > 60 * self.interval:
            return False
        return True

    def check_gif(self, local_path):
        gif = Image.open(local_path)
        try:
            gif.seek(1)
        except:  # noqa
            isanimated = False
        else:
            isanimated = True

        return isanimated

    def text_to_rgba(self, _text, path, *, dpi, **kwargs):
        # To convert a text string to an image, we can:
        # - draw it on an empty and transparent figure;
        # - save the figure to a temporary buffer using ``bbox_inches="tight",
        #   pad_inches=0`` which will pick the correct area to save;
        # - load the buffer using ``plt.imread``.
        #
        # (If desired, one can also directly save the image to the filesystem.)
        fig = Figure(facecolor="none")
        # remove last blank line
        _text = _text[: _text.rfind("\n")]
        fig.text(0, 0, _text, **kwargs)
        with BytesIO() as buf:
            fig.savefig(
                buf, dpi=dpi, format="png", bbox_inches="tight", pad_inches=0.05
            )
            buf.seek(0)
            rgba = plt.imread(buf)
        plt.imsave(path, rgba)

    def gif_to_jpg(self, local_path):
        try:
            im = Image.open(local_path)
        except OSError:
            print("Cant load", local_path)
        i = 0
        mypalette = im.getpalette()

        try:
            while 1:
                im.putpalette(mypalette)
                new_im = Image.new("RGB", im.size)
                new_im.paste(im)
                new_im.save(local_path)

                i += 1
                im.seek(im.tell() + 1)

        except:  # noqa
            pass

        return

    def convert_img(self, local_path):
        try:
            im = Image.open(local_path)
        except OSError:
            print("can't load", local_path)
        new_im = Image.new("RGB", im.size)
        new_im.paste(im)
        new_im.save(local_path)

    def download_upload_img(self, path: str, driver_id: str, link: str, name: str):
        try:
            # download image
            r = requests.get(link, stream=True)
            r.raw.decode_content = True
            # save image
            with open(f"{path}/{name}", "wb") as f:
                shutil.copyfileobj(r.raw, f)
        except:  # noqa
            return

        # if gif, change to jpg because premiere dosen't support animated image
        gif_flag = self.check_gif(f"{path}/{name}")
        if gif_flag:
            self.gif_to_jpg(f"{path}/{name}")
        else:
            self.convert_img(f"{path}/{name}")

        # upload to google drive
        self.upload_file(driver_id, f"{path}/{name}")

    def save_upload_audio(self, local_path: str, driver_id: str, text: str):
        # servide url convert txt to speech
        api_url = "https://www.yukumo.net/api/v2/aqtk1/koe.mp3"
        # cut text
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/110.0.0.0 Safari/537.36"
            "",
            # 'From': 'youremail@domain.example'  # This is another valid field
        }

        # download and upload audio
        resp = requests.get(url=api_url, params=params, headers=headers)
        with open(local_path, "wb") as f:
            f.write(resp.content)
        self.upload_file(driver_id, local_path)
        self.all_comment += text + "\n"
        return

    def save_upload_txt(self, local_path: str, driver_id: str, txt: str):
        # cut text
        if len(txt) > 140:
            txt = txt[:140]
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
        file_name = file_name.split("\\")[-1]
        file = drive.CreateFile({"title": file_name, "parents": [{"id": driver_id}]})
        file.SetContentFile(local_path)
        file.Upload()
        return file["id"]

    def run():
        pass

    def save_upload(self):
        print("downloading and uploading data set")
        # create local path
        Path(f"{self.article_path}/音声ファイル").mkdir(parents=True, exist_ok=True)
        Path(f"{self.article_path}/記事").mkdir(parents=True, exist_ok=True)
        Path(f"{self.article_path}/画像").mkdir(parents=True, exist_ok=True)
        Path(f"{self.article_path}/記事画像").mkdir(parents=True, exist_ok=True)

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
        self.image_driver_id = self.create_driver_directory(
            "画像", self.article_driver_id
        )
        self.article_image_driver_id = self.create_driver_directory(
            "記事画像", self.article_driver_id
        )

        # save image
        [
            self.download_upload_img(
                f"{self.article_path}/画像",
                self.image_driver_id,
                x,
                f"{idx + 1}_img.jpg",
            )
            for idx, x in enumerate(self.img_link)
        ]

        # download audio and comment
        name_idx = 0
        for item in self.comment_body_list:
            try:
                if not re.findall(r"\w+", item):
                    continue

                name_idx += 1
                # temp_arr = re.findall(r"\w+", item)
                # file_name = str(idx) + "_" + temp_arr[1] + temp_arr[-1]
                file_name = item
                if len(item) > 5:
                    file_name = item[:5]

                if name_idx < 10:
                    file_name = f"0{name_idx}_{file_name}"
                else:
                    file_name = f"{name_idx}_{file_name}"

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
                name_idx -= 1
                continue
        self.save_upload_txt(
            f"{self.article_path}/comments.txt",
            self.article_driver_id,
            self.all_comment,
        )
        # all_comment to image
        multi_line = iter(self.all_comment.splitlines())
        new_comment = []
        for line in multi_line:
            temp_line = ""
            while True:
                if len(line) > self.line_width:
                    temp_line += line[: self.line_width] + "\n"
                    line = line[self.line_width :]
                else:
                    temp_line += line
                    break
            new_comment.append(temp_line)

        for idx, comment in enumerate(new_comment):
            self.text_to_rgba(
                comment,
                f"{self.article_path}/記事画像/記事画像{idx}.png",
                color="yellow",
                fontsize=self.font_size,
                dpi=200,
                fontfamily="Gen Jyuu Gothic Monospace",
            )
            self.upload_file(
                self.article_image_driver_id, f"{self.article_path}/記事画像/記事画像{idx}.png"
            )

        with open(
            f"{self.article_path}/all_info.json", mode="w", encoding="utf-8"
        ) as f:
            json.dump(self.result, f, ensure_ascii=False)
        self.upload_file(self.article_driver_id, f"{self.article_path}/all_info.json")

    def run_premiere(self):
        print("running premiere")
        # copy default.prproj
        shutil.copyfile(
            "default.prproj", os.path.abspath(f"{self.article_path}/result.prproj")
        )
        os.popen('"' + os.path.abspath(f"{self.article_path}/result.prproj") + '"')

        for x in range(20):
            try:
                assert pymiere.objects.app.isDocumentOpen(), "loading"
                break
            except:  # noqa
                time.sleep(1)
                if x == 19:
                    assert False, "error running premiere"
        print("opened Premiere")
        project = pymiere.objects.app.project
        # create result sequence
        sequence = [s for s in project.sequences if s.name == "result"][0]
        project.openSequence(sequenceID=sequence.sequenceID)
        project.activeSequence

        # import files
        files_path = [
            os.path.abspath(f"{self.article_path}/音声ファイル/{x}")
            for x in os.listdir(f"{self.article_path}/音声ファイル")
        ]
        files_path += [
            os.path.abspath(f"{self.article_path}/画像/{x}")
            for x in os.listdir(f"{self.article_path}/画像")
        ]
        print("importing files")
        audio_from_seconds = 0
        image_from_seconds = 0
        for file in files_path:
            try:
                project.importFiles(
                    [file],
                    True,
                    project.rootItem,
                    True,
                )
                items = project.rootItem.findItemsMatchingMediaPath(
                    file, ignoreSubclips=False
                )
                if file[-3:] == "mp3":
                    project.activeSequence.videoTracks[0].insertClip(
                        items[0], time_from_seconds(audio_from_seconds)
                    )
                    audio_from_seconds += MP3(file).info.length - 0.5
                else:
                    items[0].setScaleToFrameSize()
                    project.activeSequence.videoTracks[0].insertClip(
                        items[0], time_from_seconds(image_from_seconds)
                    )
                    image_from_seconds += 6
            except:  # noqa
                continue

        files_path = [
            os.path.abspath(f"{self.article_path}/記事画像/{x}")
            for x in os.listdir(f"{self.article_path}/記事画像")
        ]
        image_from_seconds = 0
        for file in files_path:
            try:
                project.importFiles(
                    [file],
                    True,
                    project.rootItem,
                    True,
                )
                items = project.rootItem.findItemsMatchingMediaPath(
                    file, ignoreSubclips=False
                )
                items[0].setScaleToFrameSize()
                project.activeSequence.videoTracks[1].insertClip(
                    items[0], time_from_seconds(image_from_seconds)
                )
                image_from_seconds += 0.5
            except:  # noqa
                continue
        print("imported files")
        project.save()

        try:
            pymiere.objects.app.quit()
        except Exception as e:
            print(e)


# Base().text_to_rgba("記事画像", "1.png", color="yellow", fontsize=20, dpi=200, fontfamily="Gen Jyuu Gothic Monospace")
# print()
