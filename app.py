from flask import Flask, redirect, render_template, request, url_for
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", property_info="scraping_data")


@app.route("/run", methods=["POST"])
def scrap():
    upload_drive()
    return render_template("index.html", property_info="scraping_data")


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("index"))


def upload_drive():
    file1 = drive.CreateFile({"title": "Hello.txt"})
    file1.SetContentString("Hello")
    file1.Upload()


def download_drive():
    pass


app.run(host="0.0.0.0", debug=True, port="8080")
