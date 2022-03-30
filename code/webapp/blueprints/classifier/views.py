from flask import Blueprint, render_template
import os

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

classifier = Blueprint('classifier', __name__, template_folder="templates", static_folder="static", url_prefix="/Classifier")

@classifier.route("/")
def classifier_page():
    title="Classifier"
    img_paths = listdir_fullpath(r"blueprints\classifier\static\assets\uploads")
    return render_template("classifier.html", img_paths=img_paths, title=title)
