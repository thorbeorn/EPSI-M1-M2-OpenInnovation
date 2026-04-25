#!/bin/bash
# ── WireGuard Manager – setup & run ──────────────────────────
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$DIR/.venv"

echo ""
echo "  ⚡ WireGuard Manager"
echo "  ──────────────────────"

# Créer venv si absent
if [ ! -d "$VENV" ]; then
  echo "  → Création de l'environnement virtuel Python…"
  python3 -m venv "$VENV"
fi

# Activer
source "$VENV/bin/activate"

# Installer dépendances
echo "  → Vérification des dépendances…"
pip install -q -r "$DIR/requirements.txt"

# Vérifier socat (optionnel)
if ! command -v socat &>/dev/null; then
  echo "  ⚠  socat non trouvé (requis pour le port forwarding)"
  echo "     Installez-le avec : brew install socat"
fi

echo "  → Démarrage de l'application…"
echo ""
cd "$DIR"
python main.py
