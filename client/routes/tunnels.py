import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from flask import Blueprint, jsonify, request
from core.wireguard import (
    list_tunnels, get_tunnel, start_tunnel,
    stop_tunnel, get_tunnel_config, save_tunnel_config, generate_keypair
)

bp = Blueprint("tunnels", __name__)


@bp.get("/")
def api_list():
    return jsonify(list_tunnels())


@bp.get("/<name>")
def api_get(name):
    t = get_tunnel(name)
    if not t:
        return jsonify({"error": "not found"}), 404
    return jsonify(t)


@bp.post("/<name>/start")
def api_start(name):
    ok, msg = start_tunnel(name)
    return jsonify({"ok": ok, "message": msg}), (200 if ok else 500)


@bp.post("/<name>/stop")
def api_stop(name):
    ok, msg = stop_tunnel(name)
    return jsonify({"ok": ok, "message": msg}), (200 if ok else 500)


@bp.get("/<name>/config")
def api_config(name):
    cfg = get_tunnel_config(name)
    if cfg is None:
        return jsonify({"error": "config not found"}), 404
    return jsonify({"config": cfg})


@bp.post("/<name>/config")
def api_save_config(name):
    data = request.get_json()
    ok, msg = save_tunnel_config(name, data.get("config", ""))
    return jsonify({"ok": ok, "message": msg}), (200 if ok else 500)


@bp.get("/utils/keypair")
def api_keypair():
    return jsonify(generate_keypair())
