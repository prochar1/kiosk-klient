from flask import Flask, send_from_directory
import os

def create_app(build_dir, FLASK_PORT):
    """
    Vytvoří Flask aplikaci pouze pro servování HTML souborů.
    API endpointy jsou nyní dostupné přes window.pywebview.api.*
    """
    app = Flask(__name__, static_folder=os.path.join(build_dir, 'static'))

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):  # noqa: Flask route handler
        """Servíruje HTML soubory z build_dir."""
        if path != "" and os.path.exists(os.path.join(build_dir, path)):
            return send_from_directory(build_dir, path)
        else:
            return send_from_directory(build_dir, 'index.html')

    return app

def start_server(app, FLASK_PORT):
    from werkzeug.serving import make_server
    server = make_server('127.0.0.1', FLASK_PORT, app, threaded=True)
    server.serve_forever()
