from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", property_info="scraping_data")


@app.route("/run", methods=["POST"])
def scrap():
    
    return render_template("index.html", property_info="project")
    # return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("index"))


app.run(host="0.0.0.0", debug=True, port="8080")
