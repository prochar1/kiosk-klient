import webview

def create_window(url, flags, on_loaded):
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
        easy_drag=False
    )
    window.events.loaded += on_loaded
    return window
