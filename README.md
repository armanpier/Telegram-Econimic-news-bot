# Market Volatility & Macro News Telegram Bot

An automated Telegram bot that tracks real-time price movements across Crypto (BTC, ETH, SOL) and Precious Metals (Gold, Silver), correlates volatility with breaking macroeconomic news (Trump policy, Fed/Treasury decisions, liquidations), and publishes structured AI-driven root-cause breakdowns and scenario forecasts in Persian.

---

## Key Features

* **Dual-Window Volatility Detection:** Captures 1-hour flash moves (≥3% crypto, ≥1.2% metals) and 24-hour macro trends (≥5% crypto, ≥2% metals).
* **Zero-Cost Market Data:** Continuous feeds via Binance Public Spot API and Stooq/PAXG fallback for spot gold.
* **Targeted Macro Scraping:** Real-time Google News RSS filtering for Fed, US Treasury, White House, and crypto catalysts.
* **AI Scenario Synthesizer:** Supports DeepSeek, OpenAI, Groq, or keyless free tier fallback for structured Persian market reports.
* **Built-in `ecobot` CLI:** Manage the service and view logs directly from anywhere in your terminal.

---

## One-Line Setup (Ubuntu / Debian)

Run the automated installer:

```bash
git clone [https://github.com/armanpier/Telegram-Econimic-news-bot.git](https://github.com/armanpier/Telegram-Econimic-news-bot.git)
cd Telegram-Econimic-news-bot
chmod +x install.sh
./install.sh
```

---

## Server Management via `ecobot` CLI

Once installed, use the `ecobot` command from any directory:

```bash
ecobot logs      # Stream live monitoring & alert dispatch logs
ecobot status    # Check background daemon health
ecobot restart   # Restart the bot
ecobot stop      # Stop the service
ecobot start     # Start the service
```

---

## License
MIT License
