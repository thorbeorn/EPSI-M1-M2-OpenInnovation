"""
Vérifications système au démarrage.
Chaque check retourne : { ok, label, detail, fix }
"""

import shutil
import subprocess
import socket
import os
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckResult:
    id: str
    label: str
    ok: bool
    detail: str
    fix: Optional[str] = None   # conseil si échec
    warning: bool = False        # ok mais avec réserve

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "ok": self.ok,
            "warning": self.warning,
            "detail": self.detail,
            "fix": self.fix,
        }


# ── Checks individuels ────────────────────────────────────────────────────────

def check_internet() -> CheckResult:
    """Ping DNS Google pour vérifier la connectivité."""
    try:
        socket.setdefaulttimeout(3)
        socket.getaddrinfo("dns.google", 443)
        return CheckResult(
            id="internet",
            label="Connexion Internet",
            ok=True,
            detail="Accès réseau disponible.",
        )
    except OSError:
        return CheckResult(
            id="internet",
            label="Connexion Internet",
            ok=False,
            detail="Impossible de joindre dns.google.",
            fix="Vérifiez votre connexion réseau ou votre pare-feu.",
            warning=False,
        )


def check_wg_installed() -> CheckResult:
    """Vérifie que la commande `wg` est présente dans le PATH."""
    path = shutil.which("wg")
    if path:
        # Récupère la version
        try:
            r = subprocess.run(["wg", "--version"], capture_output=True, text=True, timeout=3)
            version = r.stdout.strip() or r.stderr.strip() or "version inconnue"
        except Exception:
            version = "version inconnue"
        return CheckResult(
            id="wg_installed",
            label="WireGuard (wg)",
            ok=True,
            detail=f"{version}  ·  {path}",
        )
    return CheckResult(
        id="wg_installed",
        label="WireGuard (wg)",
        ok=False,
        detail="Commande `wg` introuvable dans le PATH.",
        fix="macOS : brew install wireguard-tools\nLinux  : sudo apt install wireguard",
    )


def check_wg_quick() -> CheckResult:
    """Vérifie que `wg-quick` est présent."""
    path = shutil.which("wg-quick")
    if path:
        return CheckResult(
            id="wg_quick",
            label="WireGuard (wg-quick)",
            ok=True,
            detail=f"Disponible  ·  {path}",
        )
    return CheckResult(
        id="wg_quick",
        label="WireGuard (wg-quick)",
        ok=False,
        detail="Commande `wg-quick` introuvable.",
        fix="Inclus dans wireguard-tools : brew install wireguard-tools",
    )


def check_sudo_wg() -> CheckResult:
    """
    Vérifie qu'on peut exécuter `sudo wg show` sans mot de passe.
    Un avertissement suffit si sudo demande un mdp (ce n'est pas bloquant).
    """
    try:
        r = subprocess.run(
            ["sudo", "-n", "wg", "show"],
            capture_output=True, text=True, timeout=4
        )
        if r.returncode == 0:
            return CheckResult(
                id="sudo_wg",
                label="Permissions sudo (wg)",
                ok=True,
                detail="sudo wg fonctionne sans mot de passe.",
            )
        # sudo demande un mdp (returncode 1) → warning, pas bloquant
        return CheckResult(
            id="sudo_wg",
            label="Permissions sudo (wg)",
            ok=True,
            warning=True,
            detail="sudo demande un mot de passe à chaque commande.",
            fix=(
                "Pour éviter les popups, ajoutez dans /etc/sudoers via `sudo visudo` :\n"
                "%admin ALL=(ALL) NOPASSWD: /usr/bin/wg\n"
                "%admin ALL=(ALL) NOPASSWD: /usr/local/bin/wg-quick"
            ),
        )
    except FileNotFoundError:
        return CheckResult(
            id="sudo_wg",
            label="Permissions sudo (wg)",
            ok=False,
            detail="`sudo` ou `wg` introuvable.",
            fix="Installez wireguard-tools et assurez-vous que sudo est disponible.",
        )
    except subprocess.TimeoutExpired:
        return CheckResult(
            id="sudo_wg",
            label="Permissions sudo (wg)",
            ok=True,
            warning=True,
            detail="Timeout — sudo attend probablement un mot de passe.",
            fix="Configurez NOPASSWD dans /etc/sudoers pour wg et wg-quick.",
        )


def check_socat() -> CheckResult:
    """Vérifie que socat est installé (nécessaire pour le port forwarding)."""
    path = shutil.which("socat")
    if path:
        try:
            r = subprocess.run(["socat", "-V"], capture_output=True, text=True, timeout=3)
            first_line = (r.stdout or r.stderr).splitlines()[0] if (r.stdout or r.stderr) else ""
            version = first_line.strip() or "version inconnue"
        except Exception:
            version = "version inconnue"
        return CheckResult(
            id="socat",
            label="socat (port forwarding)",
            ok=True,
            detail=f"{version}  ·  {path}",
        )
    return CheckResult(
        id="socat",
        label="socat (port forwarding)",
        ok=False,
        warning=True,   # pas bloquant pour les tunnels, seulement pour les forwards
        detail="`socat` introuvable — le port forwarding sera désactivé.",
        fix="brew install socat",
    )


def check_wg_configs() -> CheckResult:
    """Vérifie si des configs WireGuard existent dans /etc/wireguard/."""
    config_dir = "/etc/wireguard"
    try:
        if not os.path.isdir(config_dir):
            return CheckResult(
                id="wg_configs",
                label="Configurations WireGuard",
                ok=True,
                warning=True,
                detail=f"{config_dir} n'existe pas encore.",
                fix="Créez /etc/wireguard/ et ajoutez vos fichiers .conf",
            )
        configs = [f for f in os.listdir(config_dir) if f.endswith(".conf")]
        count = len(configs)
        if count == 0:
            return CheckResult(
                id="wg_configs",
                label="Configurations WireGuard",
                ok=True,
                warning=True,
                detail="Aucun fichier .conf trouvé dans /etc/wireguard/",
                fix="Importez ou créez un fichier de configuration WireGuard.",
            )
        names = ", ".join(f[:-5] for f in configs[:4])
        suffix = f" (+{count-4})" if count > 4 else ""
        return CheckResult(
            id="wg_configs",
            label="Configurations WireGuard",
            ok=True,
            detail=f"{count} config(s) trouvée(s) : {names}{suffix}",
        )
    except PermissionError:
        return CheckResult(
            id="wg_configs",
            label="Configurations WireGuard",
            ok=True,
            warning=True,
            detail=f"Permission refusée pour lire {config_dir}.",
            fix="Lancez l'app avec les permissions appropriées.",
        )


# ── Runner ────────────────────────────────────────────────────────────────────

ALL_CHECKS = [
    check_internet,
    check_wg_installed,
    check_wg_quick,
    check_sudo_wg,
    check_socat,
    check_wg_configs,
]


def run_all() -> list[dict]:
    return [c().to_dict() for c in ALL_CHECKS]
