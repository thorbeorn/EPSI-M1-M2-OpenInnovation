# MyNodeHost

> **Hébergement décentralisé et intelligent — déployez vos services depuis chez vous, sans configuration réseau.**

![Statut](https://img.shields.io/badge/statut-en%20développement-yellow)
![Licence](https://img.shields.io/badge/licence-MIT-green)
![Version](https://img.shields.io/badge/version-0.1.0-blue)

---

## Table des matières

- [Présentation](#présentation)
- [Architecture](#architecture)
- [Vitrine web](#vitrine-web)
- [Structure du projet](#structure-du-projet)
- [Installation & développement local](#installation--développement-local)
- [Variables d'environnement](#variables-denvironnement)
- [À faire](#à-faire)
- [Contribuer](#contribuer)
- [Licence](#licence)

---

## Présentation

**MyNodeHost** est une solution d'hébergement décentralisée qui permet à tout utilisateur de déployer ses propres sites web et applications directement depuis un mini-serveur personnel installé chez lui, tout en bénéficiant de la puissance, de la redondance et de la simplicité du cloud.

Grâce à une technologie de tunnel réseau automatisé :

- Aucun port n'a besoin d'être ouvert sur le routeur
- Aucune configuration réseau complexe n'est requise
- L'utilisateur dispose d'une adresse IP publique et d'un nom de domaine géré par MyNodeHost

**MyNodeHost va au-delà du simple hébergement de sites.** C'est une passerelle universelle pour tout type de service personnel en ligne : sites, APIs, serveurs de jeu, bots, IoT, et bien plus.

---

## Architecture

```
[Machine cliente]                [Serveurs MyNodeHost]            [Internet]
┌──────────────┐                ┌─────────────────────┐
│  App locale  │──tunnel TLS──▶│  Reverse proxy      │──▶  203.0.113.x:PORT
│  :3000       │                │  Port mapper        │
│  API :8080   │                │  Auth / Billing     │
│  SSH :22     │                └─────────────────────┘
└──────┬───────┘
       │
  [App tunnel]
  WireGuard / TLS
```

Le client initie une **connexion sortante uniquement** — aucun port entrant requis, fonctionnel derrière tout type de NAT. Chaque tunnel est isolé et chiffré en TLS 1.3.

---

## Vitrine web

Le fichier `index.html` est la landing page statique du service.

### Sections

| Section | Description |
|---|---|
| Hero | Animation réseau canvas, stats clés, call-to-action |
| Comment ça marche | 4 étapes illustrées |
| Usages | 6 cas d'utilisation (web, API, jeux, bots, IoT, équipes) |
| Tarifs | 3 plans (Starter gratuit / Node 9€ / Cluster 29€) |
| Technologie | Terminal animé, explication du tunnel |
| Footer | Liens navigation, mentions légales |

### Technologies utilisées

- HTML5 / CSS3 vanilla — aucune dépendance externe (sauf Google Fonts)
- Canvas API pour l'animation réseau interactive en hero
- Intersection Observer pour les animations au scroll
- Polices : [Syne](https://fonts.google.com/specimen/Syne) (titres) + [IBM Plex Mono](https://fonts.google.com/specimen/IBM+Plex+Mono) (code) + [Inter](https://fonts.google.com/specimen/Inter) (corps)

### Lancer la vitrine

```bash
# Ouvrir directement dans le navigateur
open mynodehost.html

# Ou servir en local
npx serve .
# → http://localhost:3000
```

---

## Structure du projet

```
mynodehost/
├── mynodehost.html        # Vitrine / landing page
├── README.md              # Ce fichier
│
├── client/                # App client (tunnel)
│   ├── main.go            # Point d'entrée
│   ├── tunnel/            # Logique WireGuard / TLS
│   └── config/            # Config locale
│
├── server/                # Backend serveur central
│   ├── api/               # API REST de contrôle
│   ├── proxy/             # Reverse proxy + port mapper
│   ├── auth/              # Authentification & tokens
│   └── billing/           # Gestion abonnements
│
├── dashboard/             # Interface web de gestion
│   └── src/
│
└── docs/                  # Documentation technique
```

> **Note :** Les dossiers `client/`, `server/`, `dashboard/` et `docs/` sont à créer. Voir la section [À faire](#à-faire).

---

## Installation & développement local

### Prérequis

- Node.js ≥ 18 (pour la vitrine et le dashboard)
- Go ≥ 1.22 (pour le client tunnel)
- Docker (optionnel, pour le serveur central)

### Vitrine uniquement

```bash
git clone https://github.com/ton-org/mynodehost.git
cd mynodehost
open mynodehost.html
```

### Client tunnel (à venir)

```bash
cd client
go build -o mynode .
./mynode expose 3000
```

### Serveur central (à venir)

```bash
cd server
docker compose up -d
```

---

## Variables d'environnement

> Ces variables seront utilisées par le serveur central et le client. À documenter au fur et à mesure du développement.

| Variable | Description | Exemple |
|---|---|---|
| `MNH_DOMAIN` | Domaine principal du service | `mynodehost.io` |
| `MNH_SERVER_ADDR` | Adresse du serveur central | `tunnel.mynodehost.io:7000` |
| `MNH_TLS_CERT` | Chemin vers le certificat TLS | `/etc/ssl/mynodehost.crt` |
| `MNH_AUTH_SECRET` | Secret JWT pour l'API | `changeme` |
| `MNH_DB_URL` | URL de la base de données | `postgres://...` |

---

## Licence

MIT — voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

*Fabriqué avec ♥ — hébergé sur nos propres nœuds, bien sûr.*