import socket
import json
import subprocess
import shutil
import os
import sys
import time
from datetime import datetime
import threading

class Api:
    """JavaScript API pro přímé volání Python funkcí z webview."""
    
    def send_udp_message(self, message, server=None, port=None):
        """
        Pošle UDP zprávu na zadaný server a port.
        
        Args:
            message (dict): Data zprávy jako slovník/objekt
            server (str, optional): IP adresa serveru (default: '127.0.0.1')
            port (int, optional): Port serveru (default: hodnota z -outport argumentu)
            
        Returns:
            dict: {'status': 'success'/'error', 'message': str}
            
        JavaScript usage:
            window.pywebview.api.send_udp_message({type: 'test', data: 'hello'})
            window.pywebview.api.send_udp_message({type: 'test'}, '192.168.1.100', 9000)
            window.pywebview.api.send_udp_message({action: 'start'}, null, 8080)
        """
        try:
            from config import Config
            
            # Použij defaultní hodnoty pokud nejsou zadané
            if server is None:
                server = '127.0.0.1'
            if port is None:
                port = Config.ServerSendPort
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_message = json.dumps(message).encode('utf-8')
            sock.sendto(udp_message, (server, int(port)))
            sock.close()
            print(f"UDP zpráva odeslána na {server}:{port}: {message}")
            return {'status': 'success', 'message': 'UDP signal sent'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_config(self):
        """
        Vrátí aktuální konfiguraci aplikace.
        
        Returns:
            dict: Konfigurace s porty, časy a herním módem
            
        JavaScript usage:
            window.pywebview.api.get_config().then(config => console.log(config))
        """
        from config import Config, Data
        return {
            "ServerReceivePort": Config.ServerReceivePort,
            "ServerSendPort": Config.ServerSendPort,
            "TotalTime": Config.TotalTime,
            "RemainingTime": Config.RemainingTime,
            "GameMode": Data.GameMode
        }
    
    def test_connection(self):
        """
        Testovací endpoint pro ověření funkčnosti API.
        
        Returns:
            dict: Status a dostupné metody
            
        JavaScript usage:
            window.pywebview.api.test_connection().then(result => console.log(result))
        """
        return {
            'status': 'success',
            'message': 'Python API funguje',
            'available_methods': {
                'send_udp_message(server, port, **data)': 'Odesílá UDP zprávu',
                'get_config()': 'Vrací konfiguraci aplikace',
                'test_connection()': 'Testovací metoda',
                'update_html(url)': 'Aktualizuje HTML obsah'
            }
        }
    
    def update_html(self, url):
        """
        Aktualizuje HTML obsah aplikace pomocí wget.
        
        Args:
            url (str): URL pro stažení nového HTML obsahu
            
        Returns:
            dict: Status operace
            
        JavaScript usage:
            window.pywebview.api.update_html('https://example.com/new-content')
        """
        try:
            if not url:
                return {'status': 'error', 'message': 'URL parameter required'}
            
            base_path = os.path.dirname(os.path.abspath(__file__ if not getattr(sys, 'frozen', False) else sys.executable))
            html_update_dir = os.path.join(base_path, 'html_update')
            
            if os.path.exists(html_update_dir):
                return {'status': 'error', 'message': 'Update already in progress'}
            
            def run_wget():
                try:
                    print(f"Začínám wget download z {url}")
                    
                    wget_cmd = None
                    
                    # Pro PyInstaller - wget zabalený do exe
                    if getattr(sys, 'frozen', False):
                        # V PyInstaller buildu
                        wget_embedded = os.path.join(sys._MEIPASS, 'wget.exe')
                        if os.path.exists(wget_embedded):
                            wget_cmd = wget_embedded
                    
                    # Lokální wget.exe vedle aplikace (fallback)
                    if not wget_cmd:
                        local_wget = os.path.join(base_path, 'wget.exe')
                        if os.path.exists(local_wget):
                            wget_cmd = local_wget
                    
                    # Systémový wget (fallback)
                    if not wget_cmd:
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
                    
                    result = subprocess.run(cmd, cwd=base_path, capture_output=True, text=True)
                    
                    if result.returncode != 0:
                        raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
                    
                    if not os.path.exists(html_update_dir) or not os.listdir(html_update_dir):
                        raise Exception("Wget nevytvořil žádný obsah")
                    
                    html_dir = os.path.join(base_path, 'html')
                    
                    if os.path.exists(html_dir):
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        backup_dir = os.path.join(base_path, f'html_{timestamp}')
                        shutil.move(html_dir, backup_dir)
                    
                    shutil.move(html_update_dir, html_dir)
                    print(f"HTML obsah úspěšně aktualizován z {url}")
                    
                    time.sleep(2)
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                    
                except Exception as e:
                    print(f"Chyba při aktualizaci HTML: {e}")
                    if os.path.exists(html_update_dir):
                        shutil.rmtree(html_update_dir)
            
            thread = threading.Thread(target=run_wget, daemon=True)
            thread.start()
            
            return {'status': 'success', 'message': 'HTML update started'}
        
        except Exception as e:
            return {'status': 'error', 'message': str(e)}