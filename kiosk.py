import webview
from flask import Flask, send_from_directory, request, jsonify
import threading
import os
import sys
import socket
import json
import time
import subprocess
from datetime import datetime
import shutil

# --- Konfigurace Flask a cesty ---

def get_paths():
    """Získá cesty pro aplikaci."""
    if getattr(sys, 'frozen', False):
        # Produkční režim (aplikace je "zmrazena" PyInstallerem)
        base_path = os.path.dirname(os.path.abspath(sys.executable))
    else:
        # Vývojový režim (spuštěno jako .py skript)
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    build_dir = os.path.join(base_path, 'html')
    return build_dir

FLASK_PORT = 5001  # Port pro lokální server
BUILD_DIR = get_paths()

# --- Flask server pro produkční režim ---
app = Flask(__name__, static_folder=os.path.join(BUILD_DIR, 'static'))

# Globální proměnná pro okno
window = None

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
    """Pošle UDP signál s libovolnými daty."""
    try:
        data = request.get_json()
        
        # Vytvoření UDP socketu
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Získej server a port
        ip = data.get('server', '127.0.0.1')
        port = data.get('port', 8001)
        
        # Odstraň server a port z dat pro zprávu
        message = {k: v for k, v in data.items() if k not in ['server', 'port']}
        
        # Odeslání UDP zprávy
        udp_message = json.dumps(message).encode('utf-8')
        
        sock.sendto(udp_message, (ip, port))
        sock.close()
        
        print(f"UDP zpráva odeslána na {ip}:{port}: {message}")
        
        return jsonify({'status': 'success', 'message': 'UDP signal sent'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/test', methods=['GET'])
def test_api():
    """Testovací endpoint pro ověření funkčnosti API."""
    return jsonify({
        'status': 'success',
        'message': 'API funguje',
        'endpoints': {
            'GET /api/test': 'Testovací endpoint',
            'POST /api/send-udp': 'Odesílá UDP zprávu',
            'POST /api/update-html': 'Aktualizuje HTML obsah'
        }
    })

@app.route('/api/update-html', methods=['POST'])
def update_html():
    """Aktualizuje HTML obsah pomocí wget."""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'status': 'error', 'message': 'URL parameter required'}), 400
        
        base_path = os.path.dirname(os.path.abspath(__file__ if not getattr(sys, 'frozen', False) else sys.executable))
        html_update_dir = os.path.join(base_path, 'html_update')
        
        # Zkontroluj, zda neprobíhá update
        if os.path.exists(html_update_dir):
            return jsonify({'status': 'error', 'message': 'Update already in progress'}), 409
        
        # Spusť wget v novém vlákně
        def run_wget():
            try:
                print(f"Začínám wget download z {url}")
                
                # Zkus najít wget (včetně lokálního)
                wget_cmd = None
                
                # Zkus lokální wget.exe vedle aplikace
                local_wget = os.path.join(base_path, 'wget.exe')
                if os.path.exists(local_wget):
                    wget_cmd = local_wget
                else:
                    # Zkus systémový wget
                    for cmd_name in ['wget.exe', 'wget']:
                        try:
                            subprocess.run([cmd_name, '--version'], capture_output=True, check=True)
                            wget_cmd = cmd_name
                            break
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            continue
                
                if not wget_cmd:
                    raise Exception("wget není nainstalován nebo není v PATH")
                
                cmd = [
                    wget_cmd, '-nv', '--mirror', '-nH', '--html-extension', '-p',
                    '--restrict-file-names=windows', '-e', 'robots=off', '-k',
                    '--cut-dirs=2', '-P', 'html_update', url
                ]
                
                print(f"Spouštím příkaz: {' '.join(cmd)}")
                
                result = subprocess.run(cmd, cwd=base_path, capture_output=True, text=True)
                
                print(f"Wget návratový kód: {result.returncode}")
                if result.stdout:
                    print(f"Wget stdout: {result.stdout}")
                if result.stderr:
                    print(f"Wget stderr: {result.stderr}")
                
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
                
                # Zkontroluj, zda wget vytvořil nějaký obsah
                if not os.path.exists(html_update_dir) or not os.listdir(html_update_dir):
                    raise Exception("Wget nevytvořil žádný obsah")
                
                html_dir = os.path.join(base_path, 'html')
                
                # Přejmenuj stávající html složku (pouze pokud existuje)
                if os.path.exists(html_dir):
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    backup_dir = os.path.join(base_path, f'html_{timestamp}')
                    print(f"Zálohování {html_dir} -> {backup_dir}")
                    shutil.move(html_dir, backup_dir)
                
                # Přejmenuj html_update na html
                print(f"Přejmenovávání {html_update_dir} -> {html_dir}")
                shutil.move(html_update_dir, html_dir)
                
                print(f"HTML obsah úspěšně aktualizován z {url}")
                
                # Restart celé aplikace po úspěšném update
                print("Restartuji aplikaci...")
                time.sleep(2)  # Krátká pauza
                os.execv(sys.executable, [sys.executable] + sys.argv)
                
            except subprocess.CalledProcessError as e:
                print(f"Wget selhal s kódem {e.returncode}: {e.stderr}")
                # Vyčisti html_update při chybě
                if os.path.exists(html_update_dir):
                    shutil.rmtree(html_update_dir)
            except Exception as e:
                print(f"Obecná chyba při aktualizaci HTML: {e}")
                # Vyčisti html_update při chybě
                if os.path.exists(html_update_dir):
                    shutil.rmtree(html_update_dir)
        
        thread = threading.Thread(target=run_wget, daemon=True)
        thread.start()
        
        return jsonify({'status': 'success', 'message': 'HTML update started'})
    
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
    
    # Spustíme Flask server
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    print(f"Flask server spuštěn na portu {FLASK_PORT}")
    
    # Použijeme Flask server
    url = f'http://127.0.0.1:{FLASK_PORT}'
    print(f"Servíruji z adresáře '{BUILD_DIR}' na {url}")

    # Počkej chvíli než se Flask server spustí
    time.sleep(1)
    
    # Vytvoření a spuštění okna webview
    print(f"Vytvářím webview okno... ({time.time() - start_time:.2f}s)")
    
    def on_loaded():
        """Přidá F5/Ctrl+F5 handlery po načtení stránky."""
        window.evaluate_js("""
            document.addEventListener('keydown', function(e) {
                if (e.key === 'F5') {
                    e.preventDefault();
                    if (e.ctrlKey) {
                        // Ctrl+F5 - tvrdý refresh (vyčistí cache)
                        window.location.reload(true);
                    } else {
                        // F5 - normální refresh
                        window.location.reload();
                    }
                }
            });
        """)
    
    window = webview.create_window(
        'Kiosk',
        url=url,
        fullscreen=False,
        width=1920,
        height=1080,
        x=0,
        y=0,
        min_size=(1920, 1080),
        resizable=False,
        frameless=True,
        shadow=False,
        on_top=True,
        easy_drag=False
    )
    
    window.events.loaded += on_loaded

    # Spuštění GUI smyčky (blokuje, dokud se okno nezavře)
    print(f"Spouštím webview... ({time.time() - start_time:.2f}s)")
    webview.start(debug=False, http_server=False)