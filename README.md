📈 Market Volatility & Macro News Telegram Bot

An automated Telegram bot that monitors crypto and precious metals, detects major price movements, finds relevant breaking macro news, and uses AI to generate root-cause analysis and market scenarios in Persian.

✨ Features

- 📊 Real-time market monitoring
  - BTC, ETH, SOL
  - Gold & Silver
- ⚡ Automatic volatility detection
  - Crypto: "≥ 5%"
  - Precious metals: "≥ 2%"
- 📰 Breaking macro news detection
  - Trump statements
  - Federal Reserve
  - US Treasury
  - US macro policy
  - Crypto regulation
  - Market liquidations
- 🤖 AI-powered analysis
  - DeepSeek
  - OpenAI
  - Groq
  - Free/keyless fallback
- 🇮🇷 Persian-language analysis
- 🛡️ Anti-spam cooldown
  - Prevents repeated alerts during extended market moves
- 💰 Zero-cost market data
  - Binance public API
  - Stooq / Yahoo bullion feeds
  - No paid market-data API required

---

📁 Project Structure

market-volatility-bot/
├── .env.example
├── .gitignore
├── requirements.txt
├── bot.py
├── marketbot.service
└── README.md

---

🚀 Installation

1. Clone the Repository

git clone https://github.com/your-username/market-volatility-bot.git
cd market-volatility-bot

2. Create a Virtual Environment

Linux / macOS

python3 -m venv venv
source venv/bin/activate

Windows

python -m venv venv
venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

---

⚙️ Configuration

4. Create Your ".env" File

cp .env.example .env

Then open it:

nano .env

Add your configuration:

# Telegram
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_telegram_api_hash
TARGET_CHANNEL=@your_channel_username

# Volatility thresholds
CRYPTO_THRESHOLD_PCT=5.0
METALS_THRESHOLD_PCT=2.0

# Alert cooldown
COOLDOWN_HOURS=4

# AI Provider
CUSTOM_API_KEY=your_api_key
CUSTOM_API_BASE_URL=https://api.deepseek.com/v1
CUSTOM_API_MODEL=deepseek-chat

«🔐 Important: Never commit your ".env" file or API keys to GitHub.»

---

📱 Telegram Setup

You need a Telegram API ID and API hash.

Create them from:

https://my.telegram.org

Then add them to ".env":

TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_telegram_api_hash
TARGET_CHANNEL=@your_channel_username

Make sure the Telegram account running the bot has permission to post in the target channel.

---

🤖 AI Configuration

The bot supports OpenAI-compatible APIs.

DeepSeek

CUSTOM_API_KEY=your_deepseek_api_key
CUSTOM_API_BASE_URL=https://api.deepseek.com/v1
CUSTOM_API_MODEL=deepseek-chat

OpenAI

CUSTOM_API_KEY=your_openai_api_key
CUSTOM_API_BASE_URL=https://api.openai.com/v1
CUSTOM_API_MODEL=gpt-4o-mini

Other OpenAI-Compatible Providers

You can use another compatible provider by changing:

CUSTOM_API_KEY=your_api_key
CUSTOM_API_BASE_URL=https://your-provider.com/v1
CUSTOM_API_MODEL=your-model

---

▶️ Run the Bot

Start the bot:

python bot.py

On the first run, Telegram will ask you to authenticate.

Enter:

1. Your phone number
2. Telegram verification code
3. Two-factor authentication password, if enabled

After successful authentication, a Telegram session file will be created:

market_session.session

You normally won't need to authenticate again on subsequent runs.

---

🖥️ Production Deployment

For a Linux server/VPS, you can run the bot as a "systemd" service.

1. Copy the Service File

sudo cp marketbot.service /etc/systemd/system/

2. Reload systemd

sudo systemctl daemon-reload

3. Enable the Bot

sudo systemctl enable marketbot

4. Start the Bot

sudo systemctl start marketbot

5. Check Status

sudo systemctl status marketbot

6. View Live Logs

journalctl -u marketbot -f

If the bot writes to a local log file:

tail -f market_bot.log

---

🔧 Configuration Reference

Variable| Description| Example
"TELEGRAM_API_ID"| Telegram API ID| "12345678"
"TELEGRAM_API_HASH"| Telegram API hash| "your_api_hash"
"TARGET_CHANNEL"| Telegram channel| "@your_channel"
"CRYPTO_THRESHOLD_PCT"| Crypto alert threshold| "5.0"
"METALS_THRESHOLD_PCT"| Metals alert threshold| "2.0"
"COOLDOWN_HOURS"| Alert cooldown| "4"
"CUSTOM_API_KEY"| AI API key| "your_api_key"
"CUSTOM_API_BASE_URL"| AI API endpoint| "https://api.deepseek.com/v1"
"CUSTOM_API_MODEL"| AI model| "deepseek-chat"

---

📊 Default Volatility Triggers

Asset Type| Default Trigger
BTC| "≥ 5%"
ETH| "≥ 5%"
SOL| "≥ 5%"
Gold| "≥ 2%"
Silver| "≥ 2%"

The thresholds can be changed through ".env".

Example:

CRYPTO_THRESHOLD_PCT=3.0
METALS_THRESHOLD_PCT=1.5

---

🔄 How It Works

Market Data
     ↓
Price Movement Detection
     ↓
Volatility Threshold Reached
     ↓
Breaking News Search
     ↓
Macro / Catalyst Analysis
     ↓
AI Root-Cause Analysis
     ↓
Scenario Generation
     ↓
Persian Telegram Alert

---

📡 Data Sources

Cryptocurrency

Market prices are retrieved from the Binance public Spot API.

No Binance API key is required for public market data.

Precious Metals

Gold and Silver prices are retrieved through publicly available Stooq / Yahoo market data feeds.

News

Relevant breaking news is collected through Google News RSS searches focused on macroeconomic and market-moving events.

---

🧠 Example Analysis Flow

When BTC suddenly moves more than the configured threshold:

BTC moves +5.4%
       ↓
Bot detects abnormal movement
       ↓
Searches recent macro & crypto news
       ↓
Finds relevant catalyst(s)
       ↓
AI analyzes the relationship
       ↓
Generates Persian report
       ↓
Posts alert to Telegram

---

🛡️ Anti-Spam Protection

The bot includes a configurable cooldown period.

For example:

COOLDOWN_HOURS=4

If BTC triggers an alert, the bot won't repeatedly send identical alerts for the same asset during the cooldown period.

---

🔒 Security

Before deploying:

- Never commit ".env"
- Never expose Telegram API credentials
- Never expose AI API keys
- Keep "market_session.session" private
- Make sure ".gitignore" includes sensitive files

Recommended ".gitignore":

.env
*.session
__pycache__/
*.pyc
venv/
market_bot.log

---

🐛 Troubleshooting

Bot doesn't start

Check that dependencies are installed:

pip install -r requirements.txt

Telegram authentication keeps asking for login

Make sure the session file exists:

ls -la *.session

systemd service isn't starting

Check the service logs:

sudo journalctl -u marketbot -n 100 --no-pager

Check the service status:

sudo systemctl status marketbot

Environment variables aren't being loaded

Make sure ".env" exists in the directory from which the bot is configured to run:

ls -la .env

---

📜 License

MIT License.

Free to use, modify, and distribute.