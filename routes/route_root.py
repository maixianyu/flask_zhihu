from flask import (
    render_template,
    Blueprint,
    send_from_directory,
)
from config import imgDir

main = Blueprint('root', __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(imgDir, filename)
