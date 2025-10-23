# Kiosk Klient

Desktopová aplikace pro kiosk systém postavená na Python Flask backendu s webview rozhraním.

## 📋 Popis

Kiosk Klient je fullscreen aplikace určená pro kiosk systémy, která kombinuje:
- **Python Flask backend** pro API a servírování statických souborů
- **HTML/CSS/JS frontend** pro uživatelské rozhraní
- **PyWebView** pro vytvoření nativního okna aplikace
- **UDP komunikaci** pro odesílání libovolných dat
- **Wget integrace** pro automatické aktualizace obsahu

## 🚀 Funkce

- **Fullscreen kiosk rozhraní** bez rámečků a ovládacích prvků
- **UDP API** pro odesílání libovolných dat
- **Automatické aktualizace HTML** pomocí wget
- **F5/Ctrl+F5 refresh** pro obnovení obsahu
- **Automatický restart** po aktualizaci obsahu
- **Cross-platform podpora** díky PyWebView

## 🛠️ Technologie

- **Python 3.x**
- **Flask** - Web framework pro API
- **PyWebView** - Desktop GUI wrapper
- **Socket** - UDP komunikace
- **Threading** - Asynchronní běh serveru
- **Subprocess** - Wget integrace
- **PyInstaller** - Balíčkování do exe (kiosk.spec)

## 📦 Instalace

### Požadavky

```bash
pip install flask pywebview
```

### Struktura projektu

```
kiosk-klient/
├── kiosk.py          # Hlavní aplikace
├── kiosk.spec        # PyInstaller konfigurace
├── html/             # HTML build soubory
│   ├── index.html
│   └── static/
└── README.md
```

## 🎮 Použití

### Spuštění aplikace

1. Umístěte HTML obsah do složky `html/`
2. Spusťte aplikaci:

```bash
python kiosk.py
```

Nebo vytvořte exe soubor:

```bash
pyinstaller kiosk.spec
```

## 🔌 API Endpointy

### GET /api/test

Testovací endpoint pro ověření funkčnosti API.

**Response:**
```json
{
  "status": "success",
  "message": "API funguje",
  "endpoints": {
    "GET /api/test": "Testovací endpoint",
    "POST /api/send-udp": "Odesílá UDP zprávu",
    "POST /api/update-html": "Aktualizuje HTML obsah"
  }
}
```

### POST /api/send-udp

Odesílá UDP zprávu s libovolnými daty.

**Request Body:**
```json
{
  "server": "127.0.0.1",
  "port": 8001,
  "action": "custom_event",
  "data": "libovolná data",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "UDP signal sent"
}
```

**UDP zpráva:**
```json
{
  "action": "custom_event",
  "data": "libovolná data",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Poznámka:** Parametry `server` a `port` se použijí pro určení cíle UDP zprávy a nebudou součástí odeslané zprávy. Všechna ostatní data budou odeslána v UDP zprávě.

### POST /api/update-html

Aktualizuje HTML obsah aplikace stažením z URL pomocí wget.

**Request Body:**
```json
{
  "url": "https://example.com/app"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "HTML update started"
}
```

**Chování:**
- Stahuje obsah pomocí `wget` do složky `html_update`
- Po dokončení zálohuje stávající `html` složku s časovým razítkem
- Přejmenuje `html_update` na `html`
- Automaticky restartuje aplikaci pro načtení nového obsahu
- Blokuje současné spuštění více aktualizací

## ⚙️ Konfigurace

### Porty
- **Flask server**: 5001
- **UDP výchozí**: 8001

### Okno aplikace
- **Rozlišení**: 1920x1080
- **Režim**: Fullscreen, bez rámečků
- **Velikost**: Pevná (neměnitelná)

### Klávesové zkratky
- **F5**: Normální refresh stránky
- **Ctrl+F5**: Tvrdý refresh s vyčištěním cache

## 🔧 Vývoj

### Detekce prostředí

Aplikace automaticky detekuje prostředí:
- **Development**: Spuštěno jako `.py` skript - obsah ze složky `html/`
- **Production**: Spuštěno jako PyInstaller exe - obsah ze složky `html/`

### Logování

Aplikace vypisuje informace o:
- Režimu spuštění
- Čase spuštění jednotlivých komponent
- Odeslaných UDP zprávách
- Chybách při UDP komunikaci
- Wget operacích a jejich výsledcích

## 📝 Poznámky

- Aplikace běží v daemon vlákně pro Flask server
- UDP socket se automaticky uzavírá po odeslání
- Chyby při UDP komunikaci jsou zachyceny a vráceny jako JSON
- Aplikace podporuje servírování HTML Single Page Application
- HTML aktualizace běží v samostatném vlákně
- Vyžaduje `wget` nebo `wget.exe` v PATH pro funkci aktualizace
- Stará HTML data jsou automaticky zálohována s časovým razítkem
- Aplikace se automaticky restartuje po úspěšné aktualizaci obsahu
- F5/Ctrl+F5 klávesy fungují pro refresh bez závislosti na HTML obsahu

## 🤝 Přispívání

1. Fork projektu
2. Vytvořte feature branch (`git checkout -b feature/nova-funkce`)
3. Commit změny (`git commit -am 'Přidána nová funkce'`)
4. Push do branch (`git push origin feature/nova-funkce`)
5. Vytvořte Pull Request

## 📄 Licence

Tento projekt je licencován pod [MIT licencí](LICENSE).