from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/projects", methods = ["GET", "POST"])
def projects():

    return render_template("projects.html")

@app.route("/about", methods = ["GET", "POST"])
def about():

    return render_template("about.html")

@app.route("/contact", methods = ["GET", "POST"])
def contact():

    return render_template("contact.html")

@app.route("/cpp", methods = ["GET", "POST"])
def cpp():

    return render_template("cpp.html")

@app.route("/web-development", methods = ["GET", "POST"])
def webdev():
    return render_template("webdev.html")

@app.route("/python", methods = ["GET", "POST"])
def python():
    return render_template("python.html")

@app.route("/resume", methods = ["GET", "POST"])
def resume():
    return render_template("resume.html")