from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = "wg-manager-dev-key"

    from app.routes.main import bp as main_bp
    from app.routes.checks import bp as checks_bp
    from app.routes.account import bp as account_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(checks_bp, url_prefix="/api/checks")
    app.register_blueprint(account_bp, url_prefix="/api/account")

    return app
