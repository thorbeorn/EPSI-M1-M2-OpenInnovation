from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/")
def splash():
    return render_template("splash.html")


@bp.route("/app")
def index():
    return render_template("index.html")
