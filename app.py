import gdown
from flask import Flask, redirect, render_template, request, url_for
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", property_info="scraping_data")


@app.route("/upload", methods=["POST"])
def upload():
    upload_drive()
    return redirect("/")


@app.route("/download", methods=["POST"])
def download():
    download_drive()
    return redirect("/")


@app.route("/files", methods=["POST"])
def get_files():
    get_file_list()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("index"))


def upload_drive():
    file1 = drive.CreateFile({"title": "Hello.txt"})
    file1.SetContentString("Hello")
    file1.Upload()


def download_drive():
    upload_drive()
    url = "https://drive.google.com/drive/folders/1-kIcHR45LPBAxVSpXvg6rJQv4pNEghMq?usp=share_link"
    gdown.download_folder(url)


def get_file_list():
    file_list = drive.ListFile({"q": "'root' in parents and trashed=false"}).GetList()
    print(file_list)
    return file_list


app.run(host="0.0.0.0", debug=True, port="8080")
