"""
Account layer — lit mock_account.json pour l'instant.
Quand l'API centrale sera prête, seul ce fichier change.
"""

import json
import subprocess
import time
import re
from pathlib import Path
from datetime import datetime

MOCK_FILE = Path(__file__).parent.parent / "mock_account.json"
STATE_FILE = Path.home() / ".wg-manager" / "forwards.json"
HISTORY_FILE = Path.home() / ".wg-manager" / "history.json"

STATE_FILE.parent.mkdir(parents=True, exist_ok=True)


# ── Chargement mock ───────────────────────────────────────────────────────────

def _load_mock() -> dict:
    return json.loads(MOCK_FILE.read_text())


# ── Compte / profil ───────────────────────────────────────────────────────────

def get_account() -> dict:
    return _load_mock()["client"]


def get_tunnel_config() -> dict:
    return _load_mock()["tunnel"]


def get_dedicated_ips() -> list:
    return _load_mock()["dedicated_ips"]


def get_shared_ips() -> list:
    return _load_mock()["shared_ips"]


def get_dns_records() -> list:
    return _load_mock()["dns_records"]


# ── Statut tunnel (wg réel) ───────────────────────────────────────────────────

def get_tunnel_status() -> dict:
    cfg = get_tunnel_config()
    iface = cfg["interface"]

    result = {
        "interface": iface,
        "peer_endpoint": cfg["peer_endpoint"],
        "assigned_ip": cfg["assigned_ip"],
        "status": "inactive",
        "latency_ms": None,
        "last_handshake": None,
        "transfer_rx": 0,
        "transfer_tx": 0,
    }

    try:
        r = subprocess.run(
            ["sudo", "-n", "wg", "show", iface, "dump"],
            capture_output=True, text=True, timeout=4
        )
        if r.returncode == 0 and r.stdout.strip():
            lines = r.stdout.strip().splitlines()
            if len(lines) >= 2:
                # ligne peer
                parts = lines[1].split("\t")
                if len(parts) >= 8:
                    hs = int(parts[4] or 0)
                    result["last_handshake"] = hs
                    result["transfer_rx"] = int(parts[5] or 0)
                    result["transfer_tx"] = int(parts[6] or 0)
                    # handshake < 3 min = actif
                    if hs and (time.time() - hs) < 180:
                        result["status"] = "active"
    except Exception:
        pass

    # Latence ping vers le peer
    host = cfg["peer_endpoint"].split(":")[0]
    try:
        r = subprocess.run(
            ["ping", "-c", "3", "-W", "1", host],
            capture_output=True, text=True, timeout=6
        )
        m = re.search(r"avg[^=]*=\s*[\d.]+/([\d.]+)", r.stdout)
        if m:
            result["latency_ms"] = float(m.group(1))
    except Exception:
        pass

    return result


# ── Forwards (état local) ─────────────────────────────────────────────────────

def _load_forwards() -> list:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return []


def _save_forwards(data: list):
    STATE_FILE.write_text(json.dumps(data, indent=2))


def list_forwards() -> list:
    return _load_forwards()


def add_forward(data: dict) -> dict:
    forwards = _load_forwards()
    fid = f"fwd-{int(time.time())}"
    entry = {
        "id": fid,
        "label": data["label"],
        "local_port": data["local_port"],
        "internet_ip": data["internet_ip"],
        "internet_port": data["internet_port"],
        "dns_hostnames": data.get("dns_hostnames", []),
        "ip_type": data.get("ip_type", "shared"),
        "status": "stopped",
        "created_at": datetime.now().isoformat(),
    }
    forwards.append(entry)
    _save_forwards(forwards)
    _append_history("port_added", f"Port {data['local_port']}→{data['internet_port']} ajouté ({data['label']})")
    return entry


def remove_forward(fid: str):
    forwards = _load_forwards()
    removed = next((f for f in forwards if f["id"] == fid), None)
    forwards = [f for f in forwards if f["id"] != fid]
    _save_forwards(forwards)
    if removed:
        _append_history("port_removed", f"Port {removed['local_port']}→{removed['internet_port']} supprimé ({removed['label']})")


# ── Disponibilité des ports ───────────────────────────────────────────────────

def check_port_availability(internet_port: int, ip_id: str | None = None) -> dict:
    """
    Vérifie si un port est libre sur toutes nos IPs publiques.
    Retourne { available, suggested_port, conflicts }.
    """
    mock = _load_mock()
    all_ips = mock["dedicated_ips"] + mock["shared_ips"]

    if ip_id:
        all_ips = [ip for ip in all_ips if ip["id"] == ip_id]

    conflicts = []
    for ip in all_ips:
        if internet_port in ip.get("used_ports", []):
            conflicts.append({"ip": ip["address"], "label": ip["label"]})

    suggested = internet_port
    if conflicts:
        # Propose le prochain port libre (pas trop loin)
        candidate = internet_port + 1
        used_all = set()
        for ip in mock["dedicated_ips"] + mock["shared_ips"]:
            used_all.update(ip.get("used_ports", []))
        while candidate in used_all and candidate < internet_port + 50:
            candidate += 1
        suggested = candidate

    return {
        "available": len(conflicts) == 0,
        "requested_port": internet_port,
        "suggested_port": suggested,
        "conflicts": conflicts,
    }


# ── Historique ────────────────────────────────────────────────────────────────

def _load_history() -> list:
    # Combine historique mock + historique local
    mock_history = _load_mock().get("history", [])
    local_history = []
    if HISTORY_FILE.exists():
        try:
            local_history = json.loads(HISTORY_FILE.read_text())
        except Exception:
            pass
    combined = local_history + mock_history
    combined.sort(key=lambda x: x.get("ts", ""), reverse=True)
    return combined[:100]


def _append_history(event: str, detail: str):
    local_history = []
    if HISTORY_FILE.exists():
        try:
            local_history = json.loads(HISTORY_FILE.read_text())
        except Exception:
            pass
    local_history.insert(0, {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "event": event,
        "detail": detail,
    })
    HISTORY_FILE.write_text(json.dumps(local_history[:200], indent=2))


def get_history() -> list:
    return _load_history()
