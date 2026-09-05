# Market Volatility & Macro News Telegram Bot

An automated Telegram bot that tracks real-time price movements across Crypto (BTC, ETH, SOL) and Precious Metals (Gold, Silver), correlates volatility with breaking macroeconomic news (Trump statements, Fed/Treasury policy, liquidations), and publishes structured AI-driven root-cause breakdowns and scenario forecasts in Persian.

---

## Features

* **Dual-Window Volatility Detection:** Identifies both rapid 1-hour flash shocks (≥ 3% crypto, ≥ 1.2% metals) and 24-hour macro trend shifts (≥ 5% crypto, ≥ 2% metals).
* **Zero-Cost Price Feeds:** Continuous tracking via Binance Public Spot API and Stooq (with automated PAXG fallback for spot gold).
* **Targeted Breaking News:** Real-time Google News RSS scraping filtered for US Treasury, Federal Reserve, White House, and crypto catalysts.
* **AI Analysis & Scenarios:** Supports DeepSeek, OpenAI, Groq, or a built-in keyless free fallback to generate structured 4-point Persian market outlooks.
* **Anti-Spam Cooldown:** Configurable per-asset cooldown window to prevent duplicate alerts during continuous momentum.

---

## Quick Start

### 1. Clone & Install Dependencies
```bash
git clone [https://github.com/armanpier/Telegram-Econimic-news-bot.git](https://github.com/armanpier/Telegram-Econimic-news-bot.git)
cd Telegram-Econimic-news-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Interactive Setup Wizard
```bash
python setup.py
```

Follow the prompts to enter your Telegram API credentials, channel username, and alert thresholds. The wizard automatically:
* Creates your `.env` configuration.
* Authenticates your Telegram session (`market_session.session`).
* Prepares the systemd service file for background deployment.

---

## Background Deployment (Linux / systemd)

If you chose to generate a systemd service during setup, activate it with:
```bash
sudo cp /tmp/marketbot.service /etc/systemd/system/marketbot.service
sudo systemctl daemon-reload
sudo systemctl enable --now marketbot
```

Monitor live logs:
```bash
journalctl -u marketbot -f
```

---

## License
MIT License
