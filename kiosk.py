import webview
from flask import Flask, send_from_directory, request, jsonify
import threading
import os
import sys
import socket
import json
import time

# --- Konfigurace Flask a cesty ---

def get_paths():
    """Získá cesty pro vývoj a produkci."""
    if getattr(sys, 'frozen', False):
        # Produkční režim (aplikace je "zmrazena" PyInstallerem)
        base_path = os.path.dirname(os.path.abspath(sys.executable))
        build_dir = os.path.join(base_path, 'html')
        is_dev = False
    else:
        # Vývojový režim (spuštěno jako .py skript)
        base_path = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(base_path, 'html')
        is_dev = True
    return build_dir, is_dev

DEV_URL = "http://localhost:3000"  # Adresa React dev serveru
FLASK_PORT = 5001  # Port pro lokální server v produkci
BUILD_DIR, IS_DEV = get_paths()

# --- Flask server pro produkční režim ---
app = Flask(__name__, static_folder=os.path.join(BUILD_DIR, 'static'))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Servíruje React aplikaci."""
    if path != "" and os.path.exists(os.path.join(BUILD_DIR, path)):
        return send_from_directory(BUILD_DIR, path)
    else:
        return send_from_directory(BUILD_DIR, 'index.html')

@app.route('/api/send-udp', methods=['POST'])
def send_udp_signal():
    """Pošle UDP signál při ukončení hry."""
    try:
        data = request.get_json()
        
        # Vytvoření UDP socketu
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Příprava zprávy
        message = {
            'action': 'game_exit',
            'timestamp': data.get('timestamp'),
            'score': data.get('score', 0),
            'correctPlacements': data.get('correctPlacements', 0)
        }
        
        # Odeslání UDP zprávy
        udp_message = json.dumps(message).encode('utf-8')
        
        # Použij server a port z requestu
        ip = data.get('server', '127.0.0.1')
        port = data.get('port', 8001)
        
        sock.sendto(udp_message, (ip, port))
        sock.close()
        
        print(f"UDP zpráva odeslána na {ip}:{port}: {message}")
        
        return jsonify({'status': 'success', 'message': 'UDP signal sent'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# --- Spuštění serveru a Webview ---

def start_server():
    """Spustí Flask server v samostatném vlákně."""
    from werkzeug.serving import make_server
    server = make_server('127.0.0.1', FLASK_PORT, app, threaded=True)
    server.serve_forever()

if __name__ == '__main__':
    start_time = time.time()
    print(f"Spouštím aplikaci...")
    if IS_DEV:
        # Vývojový režim: Použijeme URL React dev serveru
        url = DEV_URL
        print(f"Spouštím v DEV režimu, připojuji se na {url}")
    else:
        # Produkční režim: Spustíme vlastní Flask server
        url = f'http://127.0.0.1:{FLASK_PORT}'
        print(f"Spouštím v PROD režimu, servíruji z adresáře '{BUILD_DIR}' na {url}")
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()

    # Vytvoření a spuštění okna webview
    print(f"Vytvářím webview okno... ({time.time() - start_time:.2f}s)")
    webview.create_window(
        'Kiosk',
        url=url,
        fullscreen=True,
        width=1920,
        height=1080,
        resizable=False,
        frameless=True,
        shadow=False,
        on_top=False
    )

    # Spuštění GUI smyčky (blokuje, dokud se okno nezavře)
    print(f"Spouštím webview... ({time.time() - start_time:.2f}s)")
    webview.start(debug=False, http_server=False)