# JavaScript API Dokumentace

## Přístup k Python funkcím z JavaScriptu

Všechny Python funkce jsou dostupné přes `window.pywebview.api` objekt.

### 1. Odesílání UDP zpráv

```javascript
// Základní použití
window.pywebview.api
  .send_udp_message("192.168.1.100", 9000, {
    type: "game_start",
    player_id: 123,
    timestamp: Date.now(),
  })
  .then((result) => {
    console.log("UDP Result:", result);
    // result = {status: 'success', message: 'UDP signal sent'}
  });

// S výchozími hodnotami (localhost:8001)
window.pywebview.api.send_udp_message(undefined, undefined, {
  action: "test",
  data: "hello world",
});
```

### 2. Získání konfigurace

```javascript
window.pywebview.api.get_config().then((config) => {
  console.log("Konfigurace:", config);
  // config = {
  //     ServerReceivePort: 9001,
  //     ServerSendPort: 9002,
  //     TotalTime: 3600,
  //     RemainingTime: 3600,
  //     GameMode: 'Individual'
  // }

  // Použití v aplikaci
  document.getElementById("port").textContent = config.ServerReceivePort;
});
```

### 3. Test připojení

```javascript
window.pywebview.api.test_connection().then((result) => {
  console.log("API Status:", result);
  // result = {
  //     status: 'success',
  //     message: 'Python API funguje',
  //     available_methods: {...}
  // }
});
```

### 4. Aktualizace HTML obsahu

```javascript
window.pywebview.api
  .update_html("https://example.com/new-content")
  .then((result) => {
    console.log("Update Result:", result);
    // result = {status: 'success', message: 'HTML update started'}
    // Aplikace se automaticky restartuje po dokončení
  });
```

### 5. UDP Receiver Handler

```javascript
// Globální handler pro přijaté UDP zprávy
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

function handleGameMessage(data) {
  switch (data.type) {
    case "game_start":
      startGame(data);
      break;
    case "game_end":
      endGame(data);
      break;
    default:
      console.log("Unknown message type:", data.type);
  }
}
```

### 6. Kompletní příklad použití

```javascript
// Inicializace aplikace
document.addEventListener("DOMContentLoaded", async function () {
  try {
    // Test API připojení
    const apiTest = await window.pywebview.api.test_connection();
    console.log("API dostupné:", apiTest.status === "success");

    // Načtení konfigurace
    const config = await window.pywebview.api.get_config();
    console.log("Konfigurace načtena:", config);

    // Nastavení UDP message handleru
    window.onUdpMessage = function (msg) {
      console.log("UDP Message:", msg);
      displayMessage(msg);
    };

    // Odeslání startovní zprávy
    await window.pywebview.api.send_udp_message(
      "127.0.0.1",
      config.ServerSendPort,
      {
        type: "app_ready",
        timestamp: Date.now(),
        config: config,
      }
    );
  } catch (error) {
    console.error("Chyba při inicializaci:", error);
  }
});

function displayMessage(message) {
  const messageDiv = document.createElement("div");
  messageDiv.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
  document.getElementById("messages").appendChild(messageDiv);
}
```

## Výhody nového API vs Flask endpointy:

✅ **Rychlejší** - bez HTTP overhead  
✅ **Jednodušší** - přímé volání funkcí  
✅ **Bezpečnější** - bez otevřených HTTP portů  
✅ **Nativní** - integráno do pywebview  
✅ **Asynchronní** - všechny volání vrací Promise  
✅ **Type-safe** - lepší error handling
