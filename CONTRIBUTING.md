# Přispívání do projektu

Děkujeme za váš zájem o přispívání do Kiosk Klient projektu! 

## 🚀 Jak začít

1. **Fork** tohoto repozitáře
2. **Clone** váš fork lokálně
3. **Vytvořte** novou branch pro vaši funkci
4. **Proveďte** změny
5. **Otestujte** vaše změny
6. **Commitněte** a pushněte
7. **Vytvořte** Pull Request

## 📋 Pravidla pro kód

### Python kód
- Dodržujte PEP 8 style guide
- Používejte type hints kde je to možné
- Přidejte docstrings pro nové funkce
- Udržujte funkce krátké a zaměřené na jednu věc

### Commit zprávy
- Používejte česky nebo anglicky
- Začněte s velkým písmenem
- Buďte struční ale popisní
- Příklady:
  - `Přidána podpora pro HTTPS`
  - `Opravena chyba v UDP komunikaci`
  - `Aktualizována dokumentace API`

### Pull Requests
- Popište co vaše změny dělají
- Odkažte na související issues
- Přidejte screenshoty pro UI změny
- Ujistěte se, že testy prochází

## 🧪 Testování

Před odesláním PR:

1. **Otestujte vývojový režim:**
   ```bash
   python kiosk.py
   ```

2. **Otestujte produkční režim:**
   ```bash
   pyinstaller kiosk.spec
   ./dist/kiosk.exe
   ```

3. **Otestujte UDP API:**
   - Ověřte odesílání zpráv
   - Zkontrolujte error handling

## 🐛 Hlášení chyb

Při hlášení chyby uveďte:
- Operační systém
- Python verzi
- Kroky k reprodukci
- Očekávané vs skutečné chování
- Logy/error zprávy

## 💡 Návrhy funkcí

Pro nové funkce:
- Nejdříve vytvořte issue s popisem
- Diskutujte implementaci
- Začněte s malými změnami

## 📞 Kontakt

- Vytvořte issue pro otázky
- Použijte Discussions pro obecné diskuze

Děkujeme za vaše příspěvky! 🎉