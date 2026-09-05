# Market Volatility & Macro News Telegram Bot

An automated Telegram bot that tracks real-time price movements across Crypto (BTC, ETH, SOL) and Precious Metals (Gold, Silver), correlates volatility with breaking macroeconomic news (Trump policy, Fed/Treasury decisions, liquidations), and publishes AI-driven root-cause breakdowns and scenario forecasts in Persian.

---

## Key Features

* **Dual-Window Volatility Detection:** Captures 1-hour flash moves (≥3% crypto, ≥1.2% metals) and 24-hour macro trends (≥5% crypto, ≥2% metals).
* **Zero-Cost Market Data:** Continuous feeds via Binance Public Spot API and Stooq/PAXG fallback for spot gold.
* **Targeted Macro Scraping:** Real-time Google News RSS filtering for Fed, US Treasury, White House, and crypto catalysts.
* **AI Scenario Synthesizer:** Supports DeepSeek, OpenAI, Groq, or keyless free tier fallback for structured Persian market reports.
* **Cooldown Protection:** Per-asset cooldown timer prevents repeated spam during extended market moves.

---

## One-Line Setup (Ubuntu / Debian)

Run the automated interactive installer to set up the virtual environment, credentials, and background systemd service:

```bash
git clone [https://github.com/armanpier/Telegram-Econimic-news-bot.git](https://github.com/armanpier/Telegram-Econimic-news-bot.git)
cd Telegram-Econimic-news-bot
chmod +x install.sh
./install.sh
```

---

## Service Commands

* **Live Logs:** `journalctl -u marketbot -f`
* **Restart:** `sudo systemctl restart marketbot`
* **Stop:** `sudo systemctl stop marketbot`
* **Status:** `sudo systemctl status marketbot`

---

## License
MIT License
