import threading

from flask import Flask, redirect, render_template, request, url_for

import main

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", property_info="scraping_data")


@app.route("/run", methods=["POST"])
def scrap():
    flag = request.form["flag"]
    url = request.form["url"]
    interval = request.form["interval"]
    print(flag, url, interval)

    all_thread = threading.Thread(target=main.all_run)
    # resp_thread = threading.Thread(target = re())
    all_thread.start()
    # resp_thread.start()
    # all_thread.join()
    # return resp_thread.join()
    # return render_template("index.html", property_info="project")
    # main.all_run()
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("index"))


app.run(host="0.0.0.0", debug=True, port="8080")
