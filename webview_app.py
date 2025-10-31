import webview
from python_api import Api

def create_window(url, flags, on_loaded):
    """
    Vytvoří webview okno s Python API pro přímé volání funkcí z JavaScriptu.
    
    JavaScript API dostupné jako:
    - window.pywebview.api.send_udp_message(server, port, **data)
    - window.pywebview.api.get_config()
    - window.pywebview.api.test_connection()
    - window.pywebview.api.update_html(url)
    """
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
        frameless=flags.frameless,
        shadow=False,
        on_top=flags.on_top,
        easy_drag=False,
        js_api=Api()  # Přidáváme Python API pro JavaScript
    )
    window.events.loaded += on_loaded
    return window
