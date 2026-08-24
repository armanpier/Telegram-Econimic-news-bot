# Market Volatility & Macro News Telegram Bot

Automated Telegram bot that detects rapid price movements in Crypto (BTC, ETH, SOL) and Precious Metals (Gold, Silver), correlates the surge/dump with breaking external macro news (Trump statements, Fed/Treasury policy, liquidations), and posts structured AI-generated root-cause analyses and forward-looking scenarios.

## Features
- **Real-Time Polling:** 60-second checks via Binance and Stooq free data feeds (no paid market API required).
- **Threshold Detection:** Triggers on $\ge 5\%$ crypto moves and $\ge 2\%$ precious metal moves within a 24-hour window.
- **External Breaking News Aggregation:** Scrapes real-time Google News RSS filtered for US Treasury, Fed, White House, and crypto catalysts.
- **AI Scenario Synthesizer:** Supports DeepSeek, OpenAI, Groq, or keyless free tier fallback to produce structured 4-point outlooks in Persian.
- **Spam/Cooldown Protection:** Configurable cooldown window to avoid repeated alerts for the same asset.

---

## Installation & Setup

### 1. Clone Repository & Setup Virtual Environment
```bash
git clone [https://github.com/your-username/market-volatility-bot.git](https://github.com/your-username/market-volatility-bot.git)
cd market-volatility-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
