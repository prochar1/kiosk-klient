# Kiosk Klient

Desktopová aplikace pro kiosk systém postavená na Python backendu s webview rozhraním a přímým JavaScript API.

## 📋 Popis

Kiosk Klient je fullscreen aplikace určená pro kiosk systémy, která kombinuje:

- **Python backend** s modulární architekturou
- **HTML/CSS/JS frontend** pro uživatelské rozhraní
- **PyWebView** pro vytvoření nativního okna aplikace
- **Přímé JavaScript API** pro volání Python funkcí
- **UDP komunikaci** pro odesílání a příjem zpráv
- **Wget integrace** pro automatické aktualizace obsahu

## 🚀 Funkce

- **Fullscreen kiosk rozhraní** bez rámečků a ovládacích prvků
- **Přímé JavaScript API** - volání Python funkcí bez HTTP
- **UDP komunikace** - odesílání a příjem zpráv
- **Konfigurovatelné argumenty** - porty, časy, debug režim
- **Automatické aktualizace HTML** pomocí wget
- **F5/Ctrl+F5 refresh** pro obnovení obsahu
- **Modulární architektura** - rozděleno do více souborů
- **Cross-platform podpora** díky PyWebView

## 🛠️ Technologie

- **Python 3.x**
- **Flask** - Servírování HTML souborů
- **PyWebView** - Desktop GUI wrapper s JavaScript API
- **Socket** - UDP komunikace
- **Threading** - Asynchronní běh serveru a UDP receiveru
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
├── kiosk.py              # Hlavní spouštěcí skript
├── config.py             # Konfigurace a zpracování argumentů
├── flask_server.py       # Flask server pro HTML soubory
├── python_api.py         # JavaScript API pro přímé volání Python funkcí
├── udp_receiver.py       # UDP receiver pro příjem zpráv
├── webview_app.py        # Vytvoření a správa webview okna
├── kiosk.spec            # PyInstaller konfigurace
├── wget.exe              # Wget pro Windows (volitelné)
├── html/                 # HTML build soubory
│   ├── index.html
│   └── static/
├── API_DOCUMENTATION.md  # Dokumentace JavaScript API
└── README.md
```

## 🎮 Použití

### Spuštění aplikace

1. Umístěte HTML obsah do složky `html/`
2. Spusťte aplikaci:

**Vývojový režim (s debug panel, okno s rámečkem):**

```bash
python kiosk.py -debug
```

**Produkční režim (fullscreen, bez rámečku, vždy navrchu):**

```bash
python kiosk.py
```

**S vlastními argumenty:**

```bash
python kiosk.py -inport 51000 -outport 51001 -totaltime 3600 -remainingtime 1800 -groupmode true
```

### Dostupné argumenty

| Argument                  | Popis                                                | Default    |
| ------------------------- | ---------------------------------------------------- | ---------- |
| `-debug`                  | Zapne debug režim (okno s rámečkem, developer tools) | False      |
| `-inport <port>`          | Port pro příjem UDP zpráv                            | 9001       |
| `-outport <port>`         | Port pro odesílání UDP zpráv                         | 9002       |
| `-totaltime <sec>`        | Celkový čas v sekundách                              | 3600       |
| `-remainingtime <sec>`    | Zbývající čas v sekundách                            | 3600       |
| `-groupmode <true/false>` | Herní mód (Individual/Group)                         | Individual |

### Vytvoření exe souboru

```bash
pyinstaller kiosk.spec
```

## 🔌 JavaScript API

Aplikace poskytuje přímé JavaScript API pro volání Python funkcí bez potřeby HTTP požadavků.

### Dostupné funkce

Všechny funkce jsou dostupné přes `window.pywebview.api` objekt a vrací Promise.

#### `send_udp_message(message, server?, port?)`

Odesílá UDP zprávu s libovolnými daty.

**Parametry:**

- `message` (object) - Data zprávy jako JavaScript objekt
- `server` (string, volitelný) - IP adresa serveru (default: '127.0.0.1')
- `port` (number, volitelný) - Port serveru (default: hodnota z -outport argumentu)

**JavaScript příklady:**

```javascript
// Základní použití s defaulty
await window.pywebview.api.send_udp_message({
  type: "game_start",
  player: "John",
  score: 100,
});

// S vlastním serverem a portem
await window.pywebview.api.send_udp_message(
  { type: "test", data: "hello" },
  "192.168.1.100",
  9000
);

// Pouze vlastní port
await window.pywebview.api.send_udp_message({ action: "ping" }, null, 8080);
```

#### `get_config()`

Vrací aktuální konfiguraci aplikace.

```javascript
const config = await window.pywebview.api.get_config();
console.log(config);
// {
//   ServerReceivePort: 51000,
//   ServerSendPort: 51001,
//   TotalTime: 3600,
//   RemainingTime: 3600,
//   GameMode: 'Individual'
// }
```

#### `test_connection()`

Testovací funkce pro ověření dostupnosti API.

```javascript
const result = await window.pywebview.api.test_connection();
console.log(result.status); // 'success'
```

#### `update_html(url)`

Aktualizuje HTML obsah aplikace stažením z URL pomocí wget.

```javascript
await window.pywebview.api.update_html("https://example.com/new-version");
// Aplikace se automaticky restartuje po dokončení
```

### UDP Receiver

Aplikace automaticky naslouchá UDP zprávám na portu z `-inport` argumentu a předává je do JavaScriptu.

**Nastavení handleru:**

```javascript
window.onUdpMessage = function (message) {
  console.log("Přijata UDP zpráva:", message);

  // Parsování JSON zprávy
  try {
    const data = JSON.parse(message);
    handleGameMessage(data);
  } catch (e) {
    console.log("Raw message:", message);
  }
};
```

### Kompletní příklad

```javascript
document.addEventListener("DOMContentLoaded", async function () {
  // Test API
  await window.pywebview.api.test_connection();

  // Načtení konfigurace
  const config = await window.pywebview.api.get_config();

  // Nastavení UDP handleru
  window.onUdpMessage = function (msg) {
    console.log("UDP:", msg);
  };

  // Odeslání zprávy
  await window.pywebview.api.send_udp_message({
    type: "app_ready",
    config: config,
  });
});
```

## ⚙️ Konfigurace

### Porty

- **Flask server**: 5001 (pouze pro HTML soubory)
- **UDP příjem**: 9001 (nebo hodnota z `-inport`)
- **UDP odesílání**: 9002 (nebo hodnota z `-outport`)

### Okno aplikace

- **Rozlišení**: 1920x1080
- **Vývojový režim** (`-debug`): Okno s rámečkem, developer tools
- **Produkční režim**: Fullscreen, bez rámečků, vždy navrchu
- **Velikost**: Pevná (neměnitelná)

### Klávesové zkratky

- **F5**: Normální refresh stránky
- **Ctrl+F5**: Tvrdý refresh s vyčištěním cache

### Moduly

| Modul             | Účel                                 |
| ----------------- | ------------------------------------ |
| `kiosk.py`        | Hlavní spouštěcí skript, orchestrace |
| `config.py`       | Zpracování argumentů, konfigurace    |
| `flask_server.py` | Servírování HTML souborů             |
| `python_api.py`   | JavaScript API pro přímé volání      |
| `udp_receiver.py` | Příjem UDP zpráv                     |
| `webview_app.py`  | Vytvoření webview okna               |

## 🔧 Vývoj a testování

### Detekce prostředí

Aplikace automaticky detekuje prostředí:

- **Development**: Spuštěno jako `.py` skript - obsah ze složky `html/`
- **Production**: Spuštěno jako PyInstaller exe - obsah ze složky `html/`

### Testování API

1. **Spusť aplikaci v debug režimu:**

```bash
python kiosk.py -debug -inport 51000 -outport 51001
```

2. **Otevři Developer Console (F12) a testuj:**

```javascript
// Test API připojení
await window.pywebview.api.test_connection();

// Test konfigurace
await window.pywebview.api.get_config();

// Test UDP zprávy
await window.pywebview.api.send_udp_message({
  type: "test",
  message: "Hello from JavaScript!",
});
```

3. **Sleduj UDP zprávy v terminálu:**

```bash
python -c "
import socket, json
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 51001))
print('Listening on port 51001...')
while True:
    data, addr = sock.recvfrom(1024)
    print(f'Received: {data.decode()}')
"
```

### Logování

Aplikace vypisuje informace o:

- Režimu spuštění a argumentech
- Čase spuštění jednotlivých komponent
- Flask serveru a portech
- UDP receiveru a odeslaných zprávách
- Wget operacích a jejich výsledcích
- Chybách při UDP komunikaci

## 📝 Poznámky

### Architektura

- **Modulární struktura** - kód rozdělen do logických celků
- **JavaScript API** - přímé volání Python funkcí bez HTTP
- **Flask server** - pouze pro servírování HTML souborů
- **UDP komunikace** - obousměrná (příjem i odesílání)
- **Threading** - asynchronní běh všech komponent

### Technické detaily

- Flask server běží v daemon vlákně na portu 5001
- UDP receiver běží v daemon vlákně na portu z `-inport`
- UDP socket se automaticky uzavírá po odeslání zprávy
- Chyby jsou zachyceny a vráceny jako objekty s `status` a `message`
- Podporuje HTML Single Page Application routing
- F5/Ctrl+F5 klávesy fungují pro refresh bez závislosti na HTML obsahu

### HTML aktualizace

- Běží v samostatném vlákně pro neblokování UI
- Vyžaduje `wget.exe` vedle aplikace nebo `wget` v PATH
- Stará HTML data jsou automaticky zálohována s časovým razítkem
- Aplikace se automaticky restartuje po úspěšné aktualizaci
- Blokuje současné spuštění více aktualizací

### Výhody nového API

- ✅ **Rychlejší** - bez HTTP overhead
- ✅ **Jednodušší** - přímé volání Python funkcí
- ✅ **Bezpečnější** - bez otevřených HTTP API portů
- ✅ **Nativní** - integráno do pywebview
- ✅ **Asynchronní** - všechna volání vrací Promise

## 🤝 Přispívání

1. Fork projektu
2. Vytvořte feature branch (`git checkout -b feature/nova-funkce`)
3. Commit změny (`git commit -am 'Přidána nová funkce'`)
4. Push do branch (`git push origin feature/nova-funkce`)
5. Vytvořte Pull Request

## 📄 Licence

Tento projekt je licencován pod [MIT licencí](LICENSE).
