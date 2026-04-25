import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from flask import Blueprint, jsonify, request
from core.account import (
    get_account, get_tunnel_status, get_dedicated_ips, get_shared_ips,
    get_dns_records, list_forwards, add_forward, remove_forward,
    check_port_availability, get_history
)

bp = Blueprint("account", __name__)


@bp.get("/profile")
def api_profile():
    return jsonify(get_account())


@bp.get("/tunnel")
def api_tunnel():
    return jsonify(get_tunnel_status())


@bp.get("/ips")
def api_ips():
    return jsonify({
        "dedicated": get_dedicated_ips(),
        "shared": get_shared_ips(),
    })


@bp.get("/dns")
def api_dns():
    return jsonify(get_dns_records())


@bp.get("/forwards")
def api_forwards_list():
    return jsonify(list_forwards())


@bp.post("/forwards")
def api_forwards_add():
    data = request.get_json()
    entry = add_forward(data)
    return jsonify({"ok": True, "forward": entry}), 201


@bp.delete("/forwards/<fid>")
def api_forwards_remove(fid):
    remove_forward(fid)
    return jsonify({"ok": True})


@bp.get("/ports/check")
def api_port_check():
    port = request.args.get("port", type=int)
    ip_id = request.args.get("ip_id")
    if not port:
        return jsonify({"error": "port requis"}), 400
    return jsonify(check_port_availability(port, ip_id))


@bp.get("/history")
def api_history():
    return jsonify(get_history())
