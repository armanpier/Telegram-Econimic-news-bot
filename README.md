Market Volatility & Macro News Telegram Bot

An automated Telegram bot that detects major price movements in Cryptocurrencies (BTC, ETH, SOL) and Precious Metals (Gold, Silver), correlates volatility with breaking external macro news, and posts structured AI-generated root-cause analyses and scenario predictions in Persian.

---

Features

- Zero-Cost Market Data: Continuous price tracking via Binance public Spot API and Stooq/Yahoo bullion feeds. No paid API keys required.
- Smart Volatility Triggers: Configurable triggers against rolling 24-hour baseline prices:
  - Crypto: ≥ 5%
  - Precious metals: ≥ 2%
- External Catalyst Scraping: Real-time Google News RSS scraping tailored to:
  - US macroeconomic policy
  - Trump announcements
  - Federal Reserve commentary
  - US Treasury policy
  - Crypto regulatory actions
  - Market liquidations
- AI Scenario Synthesizer: Supports DeepSeek, OpenAI, Groq, or a keyless free-tier fallback to generate a structured 4-part market breakdown.
- Anti-Spam Cooldown: Configurable per-asset cooldown window to prevent duplicate alerts during extended market momentum.
- Persian Market Analysis: Generates structured root-cause analysis and scenario predictions in Persian.

---

Project Structure

market-volatility-bot/
├── .env.example
├── .gitignore
├── requirements.txt
├── bot.py
├── marketbot.service
└── README.md

---

Installation & Setup

1. Clone the Repository & Set Up a Virtual Environment

git clone https://github.com/your-username/market-volatility-bot.git
cd market-volatility-bot

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

2. Configure Environment Variables

Copy the example environment file:

cp .env.example .env
nano .env

Fill in your credentials and configuration:

TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_telegram_api_hash
TARGET_CHANNEL=@your_channel_username

CRYPTO_THRESHOLD_PCT=5.0
METALS_THRESHOLD_PCT=2.0
COOLDOWN_HOURS=4

CUSTOM_API_KEY=your_deepseek_or_openai_key
CUSTOM_API_BASE_URL=https://api.deepseek.com/v1
CUSTOM_API_MODEL=deepseek-chat

«Important: Never commit your ".env" file or API credentials to GitHub.»

3. Initialize the Telegram Session

Run the bot once interactively to authenticate with Telegram and create the session file:

python bot.py

Enter your phone number and Telegram verification code when prompted.

A "market_session.session" file will be created after successful authentication.

---

Production Deployment with systemd

1. Copy the Service Configuration

sudo cp marketbot.service /etc/systemd/system/

2. Reload systemd and Start the Service

sudo systemctl daemon-reload
sudo systemctl enable marketbot
sudo systemctl start marketbot

3. Check Service Status

sudo systemctl status marketbot

4. Monitor Logs

Follow the systemd logs:

journalctl -u marketbot -f

Or, if the bot writes to a log file:

tail -f market_bot.log

---

Configuration

Variable| Description| Example
"TELEGRAM_API_ID"| Telegram API ID| "12345678"
"TELEGRAM_API_HASH"| Telegram API hash| "your_api_hash"
"TARGET_CHANNEL"| Telegram channel username| "@your_channel"
"CRYPTO_THRESHOLD_PCT"| Crypto volatility trigger| "5.0"
"METALS_THRESHOLD_PCT"| Precious metals volatility trigger| "2.0"
"COOLDOWN_HOURS"| Alert cooldown per asset| "4"
"CUSTOM_API_KEY"| AI provider API key| "your_api_key"
"CUSTOM_API_BASE_URL"| OpenAI-compatible API endpoint| "https://api.deepseek.com/v1"
"CUSTOM_API_MODEL"| AI model to use| "deepseek-chat"

---

Supported Assets

Cryptocurrencies

- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)

Precious Metals

- Gold
- Silver

---

How It Works

Market Data
    │
    ▼
Price Monitoring
    │
    ▼
Volatility Threshold Detection
    │
    ├── No Significant Move ──► Continue Monitoring
    │
    └── Significant Move
              │
              ▼
       Google News RSS
              │
              ▼
      Macro/Catalyst Analysis
              │
              ▼
        AI Synthesis
              │
              ▼
    Root-Cause & Scenarios
              │
              ▼
       Telegram Channel

The bot continuously monitors market prices. When an asset exceeds its configured volatility threshold, it searches for relevant breaking macroeconomic and market news, feeds the available context into the configured AI provider, and publishes a structured analysis to the target Telegram channel.

---

License

MIT License.

Free to modify and distribute.