"""
Port exposure management via socat / iptables / ssh -L.
"""

import subprocess
import json
import os
import signal
from dataclasses import dataclass, field, asdict
from typing import Optional
from pathlib import Path

STATE_FILE = Path.home() / ".wg-manager" / "port_forwards.json"
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

_procs: dict[str, subprocess.Popen] = {}  # pid actif par règle id


@dataclass
class PortForward:
    id: str
    label: str
    type: str          # "local" | "remote" | "socat"
    local_port: int
    remote_host: str
    remote_port: int
    tunnel: str        # interface wg associée
    status: str = "stopped"  # "running" | "stopped" | "error"
    pid: Optional[int] = None
    error: str = ""

    def to_dict(self):
        return asdict(self)


def _load_state() -> list[dict]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return []


def _save_state(forwards: list[dict]):
    STATE_FILE.write_text(json.dumps(forwards, indent=2))


def list_forwards() -> list[dict]:
    forwards = _load_state()
    # Mise à jour des statuts selon les PIDs actifs
    for f in forwards:
        fid = f["id"]
        if fid in _procs:
            proc = _procs[fid]
            if proc.poll() is None:
                f["status"] = "running"
                f["pid"] = proc.pid
            else:
                f["status"] = "stopped"
                f["pid"] = None
                del _procs[fid]
    return forwards


def add_forward(data: dict) -> tuple[bool, str, Optional[dict]]:
    forwards = _load_state()
    fid = f"pf-{len(forwards)+1}-{data['local_port']}"
    new = PortForward(
        id=fid,
        label=data.get("label", f"Port {data['local_port']}"),
        type=data.get("type", "socat"),
        local_port=int(data["local_port"]),
        remote_host=data["remote_host"],
        remote_port=int(data["remote_port"]),
        tunnel=data.get("tunnel", ""),
    )
    forwards.append(new.to_dict())
    _save_state(forwards)
    return True, "Règle ajoutée.", new.to_dict()


def remove_forward(fid: str) -> tuple[bool, str]:
    forwards = _load_state()
    stop_forward(fid)
    forwards = [f for f in forwards if f["id"] != fid]
    _save_state(forwards)
    return True, "Règle supprimée."


def start_forward(fid: str) -> tuple[bool, str]:
    forwards = _load_state()
    rule = next((f for f in forwards if f["id"] == fid), None)
    if not rule:
        return False, "Règle introuvable."

    cmd = [
        "socat",
        f"TCP-LISTEN:{rule['local_port']},fork,reuseaddr",
        f"TCP:{rule['remote_host']}:{rule['remote_port']}",
    ]

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _procs[fid] = proc
        # Mise à jour état
        for f in forwards:
            if f["id"] == fid:
                f["status"] = "running"
                f["pid"] = proc.pid
        _save_state(forwards)
        return True, f"Forward démarré (PID {proc.pid})."
    except FileNotFoundError:
        return False, "socat non trouvé. Installez-le : brew install socat"
    except Exception as e:
        return False, str(e)


def stop_forward(fid: str) -> tuple[bool, str]:
    if fid in _procs:
        proc = _procs[fid]
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
        del _procs[fid]

    forwards = _load_state()
    for f in forwards:
        if f["id"] == fid:
            f["status"] = "stopped"
            f["pid"] = None
    _save_state(forwards)
    return True, "Forward arrêté."
