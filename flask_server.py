from flask import Flask, send_from_directory, request, jsonify
import os
import socket
import json
import subprocess
import shutil
from datetime import datetime
import time
import threading

def create_app(build_dir, FLASK_PORT):
    app = Flask(__name__, static_folder=os.path.join(build_dir, 'static'))

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(build_dir, path)):
            return send_from_directory(build_dir, path)
        else:
            return send_from_directory(build_dir, 'index.html')

    @app.route('/api/send-udp', methods=['POST'])
    def send_udp_signal():
        try:
            data = request.get_json()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ip = data.get('server', '127.0.0.1')
            port = data.get('port', 8001)
            message = {k: v for k, v in data.items() if k not in ['server', 'port']}
            udp_message = json.dumps(message).encode('utf-8')
            sock.sendto(udp_message, (ip, port))
            sock.close()
            print(f"UDP zpráva odeslána na {ip}:{port}: {message}")
            return jsonify({'status': 'success', 'message': 'UDP signal sent'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/api/test', methods=['GET'])
    def test_api():
        return jsonify({
            'status': 'success',
            'message': 'API funguje',
            'endpoints': {
                'GET /api/test': 'Testovací endpoint',
                'POST /api/send-udp': 'Odesílá UDP zprávu',
                'POST /api/update-html': 'Aktualizuje HTML obsah'
            }
        })

    # ...další endpointy podle potřeby...

    return app

def start_server(app, FLASK_PORT):
    from werkzeug.serving import make_server
    server = make_server('127.0.0.1', FLASK_PORT, app, threaded=True)
    server.serve_forever()
