import socket
import threading
import time
import json

def start_udp_receiver(window, port):
    def udp_thread():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', port))
        print(f"UDP receiver naslouchá na portu {port}")
        while True:
            try:
                data, addr = sock.recvfrom(4096)
                msg = data.decode('utf-8')
                print(f"Přijata UDP zpráva od {addr}: {msg}")
                if window is not None:
                    js_code = f"window.onUdpMessage && window.onUdpMessage({json.dumps(msg)});"
                    window.evaluate_js(js_code)
            except Exception as e:
                print(f"Chyba v UDP receiveru: {e}")
                time.sleep(1)
    thread = threading.Thread(target=udp_thread, daemon=True)
    thread.start()
