
# Whatsnium

**Whatsnium** is a Python package to automate WhatsApp Web messaging using Selenium with multi-language support via YAML.

---

⚠️ **Important Notice**

Whatsnium is intended for personal or experimental use only.  
**Do not use this tool for mass messaging, spamming, or production environments**, as this violates WhatsApp's [Terms of Service](https://www.whatsapp.com/legal/terms-of-service). Abuse of automation tools may result in your number being **banned** from WhatsApp.  
Use responsibly.

---

## 🚀 Features

- ✅ Send messages to your WhatsApp contacts automatically.
- ✅ Read recent messages from any chat.
- ✅ Multilingual interface support using YAML (PT-BR, EN, ES, and more).
- ✅ Easily extendable to more languages!

## ⚙️ Installation

```bash
pip install whatsnium
```

Or install directly from source:

```bash
git clone https://github.com/yourusername/whatsnium.git
cd whatsnium
pip install .
```

## 🧠 Requirements

- Python 3.7+
- Google Chrome installed
- [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/) compatible with your Chrome version
- `PyYAML` and `selenium`

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🌐 YAML-Based Language Labels

To support multiple languages, we use a `labels.yaml` file:

```yaml
search_input:
  - "Search input textbox"
  - "Caixa de texto de pesquisa"
  - "Cuadro de texto de búsqueda"

message_input:
  - "Type a message"
  - "Digite uma mensagem"
  - "Escribe un mensaje"
```

You can customize or add more labels for additional languages!


## 🧪 Example (Python)

```python
from whatsnium import Whatsnium

bot = Whatsnium(driver_path="chromedriver", label_file="labels.yaml")
bot.start_driver()
bot.wait_for_login(30)
bot.send_message("Friend Name", "Hello from Whatsnium!")
messages = bot.read_last_messages("Friend Name", 5)
print(messages)
bot.close()
```

## 📜 License

MIT License