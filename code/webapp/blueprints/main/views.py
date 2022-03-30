from flask import Blueprint, render_template

main = Blueprint('main', __name__, template_folder="templates", static_folder="static")

@main.route("/")
def index():
    title="Home"
    return render_template("index.html", title=title)