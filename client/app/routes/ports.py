import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from flask import Blueprint, jsonify, request
from core.ports import list_forwards, add_forward, remove_forward, start_forward, stop_forward

bp = Blueprint("ports", __name__)


@bp.get("/")
def api_list():
    return jsonify(list_forwards())


@bp.post("/")
def api_add():
    data = request.get_json()
    ok, msg, rule = add_forward(data)
    return jsonify({"ok": ok, "message": msg, "rule": rule}), (201 if ok else 400)


@bp.delete("/<fid>")
def api_remove(fid):
    ok, msg = remove_forward(fid)
    return jsonify({"ok": ok, "message": msg})


@bp.post("/<fid>/start")
def api_start(fid):
    ok, msg = start_forward(fid)
    return jsonify({"ok": ok, "message": msg}), (200 if ok else 500)


@bp.post("/<fid>/stop")
def api_stop(fid):
    ok, msg = stop_forward(fid)
    return jsonify({"ok": ok, "message": msg})
