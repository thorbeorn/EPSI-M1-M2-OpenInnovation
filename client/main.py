#!/usr/bin/env python3
"""
WireGuard Manager
Affiche la splash screen pendant que Flask démarre,
puis redirige automatiquement vers l'interface principale.
"""

import threading
import time
import webview
from app import create_app

flask_app = create_app()
flask_ready = threading.Event()


def start_flask():
    @flask_app.before_request
    def mark_ready():
        flask_ready.set()

    flask_app.run(host="127.0.0.1", port=5174, debug=False, use_reloader=False)


def wait_and_redirect(window):
    """Attend que Flask soit prêt puis navigue vers l'app."""
    flask_ready.wait(timeout=10)
    time.sleep(0.8)  # laisse la splash visible un instant
    window.load_url("http://127.0.0.1:5174/app")


def main():
    # Démarre Flask en arrière-plan
    t = threading.Thread(target=start_flask, daemon=True)
    t.start()

    # Attend que le port soit ouvert
    import socket
    for _ in range(20):
        try:
            s = socket.create_connection(("127.0.0.1", 5174), timeout=0.3)
            s.close()
            break
        except OSError:
            time.sleep(0.15)

    # Fenêtre sur la splash
    window = webview.create_window(
        title="WireGuard Manager",
        url="http://127.0.0.1:5174/",
        width=1200,
        height=800,
        min_size=(900, 600),
        resizable=True,
        background_color="#080c10",
    )

    # Redirige vers l'app une fois prêt
    threading.Thread(target=wait_and_redirect, args=(window,), daemon=True).start()

    webview.start(debug=False)


if __name__ == "__main__":
    main()
