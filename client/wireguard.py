"""
Core WireGuard tunnel management.
Wraps wg / wg-quick system commands.
"""

import subprocess
import json
import os
import re
from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path

WG_CONFIG_DIR = Path("/etc/wireguard")


@dataclass
class Tunnel:
    name: str
    status: str          # "active" | "inactive" | "error"
    public_key: str = ""
    endpoint: str = ""
    allowed_ips: str = ""
    latest_handshake: str = ""
    transfer_rx: int = 0
    transfer_tx: int = 0
    peers: int = 0

    def to_dict(self):
        return asdict(self)


def _run(cmd: list[str], sudo: bool = True) -> tuple[int, str, str]:
    if sudo:
        cmd = ["sudo"] + cmd
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def list_tunnels() -> list[dict]:
    """Liste toutes les interfaces WireGuard disponibles."""
    tunnels = []

    # Interfaces actives via `wg show`
    rc, out, _ = _run(["wg", "show", "all", "dump"])
    active_ifaces: dict[str, dict] = {}

    if rc == 0 and out.strip():
        for line in out.strip().splitlines():
            parts = line.split("\t")
            if len(parts) >= 4:
                iface = parts[0]
                if iface not in active_ifaces:
                    active_ifaces[iface] = {
                        "public_key": parts[1],
                        "peers": 0,
                        "transfer_rx": 0,
                        "transfer_tx": 0,
                        "latest_handshake": "",
                        "endpoint": "",
                    }
                else:
                    # Ligne peer
                    active_ifaces[iface]["peers"] += 1
                    if len(parts) >= 8:
                        active_ifaces[iface]["transfer_rx"] += int(parts[6] or 0)
                        active_ifaces[iface]["transfer_tx"] += int(parts[7] or 0)
                        if parts[5] and parts[5] != "0":
                            active_ifaces[iface]["latest_handshake"] = parts[5]
                        if parts[3] and parts[3] != "(none)":
                            active_ifaces[iface]["endpoint"] = parts[3]

    # Configs disponibles dans /etc/wireguard/
    config_ifaces = set()
    if WG_CONFIG_DIR.exists():
        for f in WG_CONFIG_DIR.glob("*.conf"):
            config_ifaces.add(f.stem)

    all_ifaces = set(active_ifaces.keys()) | config_ifaces

    for iface in sorted(all_ifaces):
        info = active_ifaces.get(iface, {})
        tunnels.append(Tunnel(
            name=iface,
            status="active" if iface in active_ifaces else "inactive",
            public_key=info.get("public_key", ""),
            endpoint=info.get("endpoint", ""),
            peers=info.get("peers", 0),
            transfer_rx=info.get("transfer_rx", 0),
            transfer_tx=info.get("transfer_tx", 0),
            latest_handshake=info.get("latest_handshake", ""),
        ).to_dict())

    return tunnels


def get_tunnel(name: str) -> Optional[dict]:
    tunnels = list_tunnels()
    return next((t for t in tunnels if t["name"] == name), None)


def start_tunnel(name: str) -> tuple[bool, str]:
    rc, _, err = _run(["wg-quick", "up", name])
    if rc == 0:
        return True, f"Tunnel {name} démarré."
    return False, err.strip() or "Erreur inconnue"


def stop_tunnel(name: str) -> tuple[bool, str]:
    rc, _, err = _run(["wg-quick", "down", name])
    if rc == 0:
        return True, f"Tunnel {name} arrêté."
    return False, err.strip() or "Erreur inconnue"


def get_tunnel_config(name: str) -> Optional[str]:
    path = WG_CONFIG_DIR / f"{name}.conf"
    if path.exists():
        rc, out, _ = _run(["cat", str(path)])
        if rc == 0:
            return out
    return None


def save_tunnel_config(name: str, config: str) -> tuple[bool, str]:
    path = WG_CONFIG_DIR / f"{name}.conf"
    try:
        rc, _, err = _run(["bash", "-c", f"echo {json.dumps(config)} > {path}"])
        if rc == 0:
            return True, "Configuration sauvegardée."
        return False, err
    except Exception as e:
        return False, str(e)


def generate_keypair() -> dict:
    rc, privkey, _ = _run(["wg", "genkey"])
    if rc != 0:
        return {}
    privkey = privkey.strip()
    rc2, pubkey, _ = _run(["bash", "-c", f"echo {privkey} | wg pubkey"])
    return {
        "private_key": privkey,
        "public_key": pubkey.strip() if rc2 == 0 else "",
    }
