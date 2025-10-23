# Kiosk Klient

Desktopová aplikace pro kiosk systém postavená na Python Flask backendu a React frontendu s webview rozhraním.

## 📋 Popis

Kiosk Klient je fullscreen aplikace určená pro kiosk systémy, která kombinuje:
- **Python Flask backend** pro API a servírování statických souborů
- **React frontend** (předpokládaný) pro uživatelské rozhraní
- **PyWebView** pro vytvoření nativního okna aplikace
- **UDP komunikaci** pro odesílání herních dat

## 🚀 Funkce

- **Dual režim**: Vývojový (připojení na React dev server) a produkční (vlastní Flask server)
- **Fullscreen kiosk rozhraní** bez rámečků a ovládacích prvků
- **UDP API** pro odesílání herních statistik
- **Automatická detekce prostředí** (development vs production)
- **Cross-platform podpora** díky PyWebView

## 🛠️ Technologie

- **Python 3.x**
- **Flask** - Web framework pro API
- **PyWebView** - Desktop GUI wrapper
- **Socket** - UDP komunikace
- **Threading** - Asynchronní běh serveru
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
├── html/             # React build soubory (produkce)
│   ├── index.html
│   └── static/
└── README.md
```

## 🎮 Použití

### Vývojový režim

Pro vývoj s React dev serverem (port 3000):

```bash
python kiosk.py
```

Aplikace se automaticky připojí na `http://localhost:3000`

### Produkční režim

Pro produkci s vlastním Flask serverem:

1. Umístěte React build do složky `html/`
2. Spusťte aplikaci:

```bash
python kiosk.py
```

Nebo vytvořte exe soubor:

```bash
pyinstaller kiosk.spec
```

## 🔌 API Endpointy

### POST /api/send-udp

Odesílá UDP zprávu s herními daty.

**Request Body:**
```json
{
  "server": "127.0.0.1",
  "port": 8001,
  "timestamp": "2024-01-01T12:00:00Z",
  "score": 100,
  "correctPlacements": 5
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
  "action": "game_exit",
  "timestamp": "2024-01-01T12:00:00Z",
  "score": 100,
  "correctPlacements": 5
}
```

## ⚙️ Konfigurace

### Porty
- **Flask server**: 5001 (produkce)
- **React dev server**: 3000 (vývoj)
- **UDP výchozí**: 8001

### Okno aplikace
- **Rozlišení**: 1920x1080
- **Režim**: Fullscreen, bez rámečků
- **Velikost**: Pevná (neměnitelná)

## 🔧 Vývoj

### Detekce prostředí

Aplikace automaticky detekuje prostředí:
- **Development**: Spuštěno jako `.py` skript
- **Production**: Spuštěno jako PyInstaller exe

### Logování

Aplikace vypisuje informace o:
- Režimu spuštění (DEV/PROD)
- Čase spuštění jednotlivých komponent
- Odeslaných UDP zprávách
- Chybách při UDP komunikaci

## 📝 Poznámky

- Aplikace běží v daemon vlákně pro Flask server
- UDP socket se automaticky uzavírá po odeslání
- Chyby při UDP komunikaci jsou zachyceny a vráceny jako JSON
- Aplikace podporuje servírování React Single Page Application

## 🤝 Přispívání

1. Fork projektu
2. Vytvořte feature branch (`git checkout -b feature/nova-funkce`)
3. Commit změny (`git commit -am 'Přidána nová funkce'`)
4. Push do branch (`git push origin feature/nova-funkce`)
5. Vytvořte Pull Request

## 📄 Licence

Tento projekt je licencován pod [MIT licencí](LICENSE).