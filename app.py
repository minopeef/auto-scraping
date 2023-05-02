import threading

from flask import Flask, redirect, render_template, request, url_for, jsonify

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
    flag = request.form["flag"]
    url = request.form["url"]
    interval = request.form["interval"]
    print(flag, url, interval)
    if Store.flag == False:
        if Store.status == "stopped":
            ThreadFlag.all_thread.join()
            # threading.Thread(target=duplicate_thread, args=(ThreadFlag.all_thread, interval)).start()
        ThreadFlag.all_thread = threading.Thread(target=main.all_run, args=(interval,))
        ThreadFlag.all_thread.start()
        Store.flag = True
        Store.status = "started"
    else:
        Store.status = "running"
    
    return jsonify({ 'status': Store.status })


    if flag == "auto":
        if Store.Auto.flag == False:
            # all_thread = threading.Thread(target=main.all_run, args=(interval))
            # all_thread.start()
            Store.Auto.flag = True
            Store.Auto.status = "started"
        else:
            Store.Auto.status = "running"
        # return redirect(url_for("index"))
        return jsonify({ 'status': Store.Auto.status })
    if flag == "manual":
        if Store.Manual.flag == False:
            Store.Manual.flag = True
            Store.Auto.status = "started"
        else:
            Store.Manual.status = "running"
        return jsonify({ 'status': Store.Manual.status })

@app.route("/stop", methods=["POST"])
def stop():
    flag = request.form["flag"]
    Store.flag = False
    Store.status = "stopped"
    return jsonify({ 'status': Store.status })
    if flag == "auto":
        Store.Auto.flag = False
        Store.Auto.status = "stopped"
        return jsonify({ 'status': Store.Auto.status })
    if flag == "manual":
        Store.Manual.flag = False
        Store.Manual.status = "stopped"
        return jsonify({ 'status': Store.Manual.status })
    # return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("index"))


app.run(host="0.0.0.0", debug=True, port="8080")
