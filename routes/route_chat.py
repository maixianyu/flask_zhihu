from flask import (
    render_template,
    Blueprint,
)
from routes.route_user import login_required


main = Blueprint('chat', __name__)


@main.route("/")
@login_required
def index():
    return render_template("chat/index.html")
