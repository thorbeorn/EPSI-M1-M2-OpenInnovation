import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from flask import Blueprint, jsonify, Response
from core.checks import ALL_CHECKS
import json

bp = Blueprint("checks", __name__)


@bp.get("/")
def api_all():
    """Retourne tous les checks d'un coup."""
    from core.checks import run_all
    return jsonify(run_all())


@bp.get("/stream")
def api_stream():
    """
    SSE — envoie chaque check au fur et à mesure qu'il s'exécute.
    Le frontend reçoit les résultats en temps réel.
    """
    def generate():
        for check_fn in ALL_CHECKS:
            result = check_fn()
            data = json.dumps(result.to_dict())
            yield f"data: {data}\n\n"
        # Signal de fin
        yield "data: {\"id\":\"__done__\"}\n\n"

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )
