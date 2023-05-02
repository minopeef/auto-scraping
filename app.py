import threading

from flask import Flask, jsonify, redirect, render_template, request, url_for

import main
from store import Store

app = Flask(__name__)


class ThreadFlag:
    all_thread = None


# def duplicate_thread(_thread, interval):
#     _thread.join()
#     ThreadFlag.all_thread = threading.Thread(target=main.all_run, args = (interval)).start()
#     ThreadFlag.all_thread.start()


@app.route("/")
def index():
    if Store.mode == "Auto":
        return render_template("index.html", status=Store.Auto.status)
    if Store.mode == "Manual":
        return render_template("index.html", status=Store.Manual.status)


@app.route("/run", methods=["POST"])
def scrap():
    url = request.form["url"]
    interval = request.form["interval"]
    mode = request.form["flag"]
    print(mode, url, interval)
    if Store.flag == False:
        if (
            ThreadFlag.all_thread
            and ThreadFlag.all_thread.is_alive()
            and Store.status == "stopped"
        ):
            return jsonify({"status": "rerun 5min"})
        if mode == "manual":
            ThreadFlag.all_thread = threading.Thread(
                target=main.manual_run, args=(url,)
            )
        else:
            ThreadFlag.all_thread = threading.Thread(
                target=main.all_run, args=(interval,)
            )
            ThreadFlag.all_thread.start()
        Store.flag = True
        Store.status = "started"
    else:
        Store.status = "running"

    return jsonify({"status": Store.status})


@app.route("/stop", methods=["POST"])
def stop():
    flag = request.form["flag"]
    Store.flag = False
    Store.status = "stopped"
    return jsonify({"status": Store.status})


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("index"))


app.run(host="0.0.0.0", debug=True, port="80")
