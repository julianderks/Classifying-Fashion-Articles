from flask import Blueprint, render_template


about = Blueprint('about', __name__, template_folder="templates", static_folder="static", url_prefix="/About")

@about.route("/")
def about_page():
    title="About"
    return render_template("about.html", title=title)