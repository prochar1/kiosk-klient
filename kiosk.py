import sys
import os
import time
import threading
import json
from config import Config, AppFlags, Data, parse_arguments
from flask_server import create_app, start_server
from udp_receiver import start_udp_receiver
from webview_app import create_window

def get_paths():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(os.path.abspath(sys.executable))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(base_path, 'html')
    return build_dir

FLASK_PORT = 5001
BUILD_DIR = get_paths()

if __name__ == '__main__':
    parse_arguments(sys.argv[1:])
    start_time = time.time()
    print(f"Spouštím aplikaci...")

    app = create_app(BUILD_DIR, FLASK_PORT)
    server_thread = threading.Thread(target=start_server, args=(app, FLASK_PORT), daemon=True)
    server_thread.start()
    print(f"Flask server spuštěn na portu {FLASK_PORT}")

    url = f'http://127.0.0.1:{FLASK_PORT}'
    print(f"Servíruji z adresáře '{BUILD_DIR}' na {url}")
    time.sleep(1)

    def on_loaded():
        js_config = json.dumps({
            "ServerReceivePort": Config.ServerReceivePort,
            "ServerSendPort": Config.ServerSendPort,
            "TotalTime": Config.TotalTime,
            "RemainingTime": Config.RemainingTime,
            "GameMode": Data.GameMode
        })
        window.evaluate_js(f"window.kioskConfig = {js_config};")
        window.evaluate_js("""
            document.addEventListener('keydown', function(e) {
                if (e.key === 'F5') {
                    e.preventDefault();
                    if (e.ctrlKey) {
                        window.location.reload(true);
                    } else {
                        window.location.reload();
                    }
                }
            });
        """)

    window = create_window(url, AppFlags, on_loaded)
    start_udp_receiver(window, Config.ServerReceivePort)

    print(f"Spouštím webview... ({time.time() - start_time:.2f}s)")
    import webview
    webview.start(debug=AppFlags.debug, http_server=False)