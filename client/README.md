# ⚡ WireGuard Manager

Application desktop (macOS / Linux) pour gérer les tunnels WireGuard et l'exposition de ports.  
Interface web embarquée via **pywebview** (WebKit natif) + serveur **Flask** local.

## Stack
- **Python 3.10+** — pas d'Electron, pas de Node.js
- **Flask** — serveur HTTP local sur `127.0.0.1:5174`
- **pywebview** — fenêtre native WebKit (macOS) / GTKWebKit (Linux)
- **socat** — port forwarding TCP

## Pré-requis

```bash
# macOS
brew install wireguard-tools socat

# Python 3.10+
python3 --version
```

## Installation & lancement

```bash
git clone https://github.com/VOUS/wg-manager
cd wg-manager
chmod +x run.sh
./run.sh
```

Le script crée automatiquement un venv et installe les dépendances.

## Structure

```
wg-manager/
├── main.py              # Point d'entrée — Flask + WebView
├── run.sh               # Script de lancement (macOS/Linux)
├── requirements.txt
├── app/
│   ├── __init__.py      # Factory Flask
│   ├── routes/
│   │   ├── main.py      # Sert l'interface HTML
│   │   ├── tunnels.py   # API /api/tunnels/
│   │   └── ports.py     # API /api/ports/
│   └── templates/
│       └── index.html   # SPA complète (HTML/CSS/JS)
└── core/
    ├── wireguard.py     # wg / wg-quick wrapper
    └── ports.py         # socat port forwarding
```

## API REST

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/tunnels/` | Liste les tunnels |
| POST | `/api/tunnels/:name/start` | Démarre un tunnel |
| POST | `/api/tunnels/:name/stop` | Arrête un tunnel |
| GET | `/api/tunnels/:name/config` | Lit la config wg.conf |
| POST | `/api/tunnels/:name/config` | Sauvegarde la config |
| GET | `/api/tunnels/utils/keypair` | Génère une paire de clés |
| GET | `/api/ports/` | Liste les forwards |
| POST | `/api/ports/` | Ajoute un forward |
| POST | `/api/ports/:id/start` | Démarre un forward |
| POST | `/api/ports/:id/stop` | Arrête un forward |
| DELETE | `/api/ports/:id` | Supprime un forward |

## Permissions sudo

Les commandes `wg` et `wg-quick` nécessitent des droits root.  
Ajoutez ces lignes dans `/etc/sudoers` (via `sudo visudo`) :

```
%admin ALL=(ALL) NOPASSWD: /usr/bin/wg
%admin ALL=(ALL) NOPASSWD: /usr/local/bin/wg-quick
```
