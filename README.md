

📈 Market Volatility & Macro News Telegram Bot

An automated Telegram bot that monitors Cryptocurrencies (BTC, ETH, SOL) and Precious Metals (Gold, Silver), detects major price movements, correlates them with breaking macro news, and generates AI-powered root-cause analysis and scenario predictions in Persian.

---

✨ Features

· 📊 Real-time monitoring of:
  · Bitcoin (BTC)
  · Ethereum (ETH)
  · Solana (SOL)
  · Gold
  · Silver
· ⚡ Configurable volatility triggers
  · Crypto: ≥ 5%
  · Precious metals: ≥ 2%
· 📰 Breaking macro news detection
  · Trump statements
  · Federal Reserve
  · US Treasury
  · US macro policy
  · Crypto regulation
  · Market liquidations
· 🤖 AI-powered analysis
  · DeepSeek
  · OpenAI
  · Groq
  · Free/keyless fallback
· 🇮🇷 Persian-language market analysis
· 🛡️ Anti-spam cooldown
· 💰 Zero-cost market data
· 🔑 No paid market-data API required

---

🚀 Installation

1. Clone the Repository

```bash
git clone https://github.com/your-username/market-volatility-bot.git
cd market-volatility-bot
```

2. Create a Virtual Environment

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

⚙️ Configuration

4. Create the .env File

Linux / macOS

```bash
cp .env.example .env
```

Then open it:

```bash
nano .env
```

Add your configuration:

```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_telegram_api_hash
TARGET_CHANNEL=@your_channel_username

CRYPTO_THRESHOLD_PCT=5.0
METALS_THRESHOLD_PCT=2.0
COOLDOWN_HOURS=4

CUSTOM_API_KEY=your_api_key
CUSTOM_API_BASE_URL=https://api.deepseek.com/v1
CUSTOM_API_MODEL=deepseek-chat
```

Important: Never commit your .env file or API keys to GitHub.

---

📱 Telegram Setup

You need a Telegram API ID and API hash.

1. Go to https://my.telegram.org
2. Log in with your Telegram account.
3. Open API Development Tools.
4. Create an application.
5. Copy your API ID and API Hash.

Add them to your .env file:

```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_telegram_api_hash
TARGET_CHANNEL=@your_channel_username
```

The Telegram account running the bot must have permission to post messages in the target channel.

---

🤖 AI Configuration

The bot supports OpenAI-compatible APIs.

DeepSeek

```env
CUSTOM_API_KEY=your_deepseek_api_key
CUSTOM_API_BASE_URL=https://api.deepseek.com/v1
CUSTOM_API_MODEL=deepseek-chat
```

OpenAI

```env
CUSTOM_API_KEY=your_openai_api_key
CUSTOM_API_BASE_URL=https://api.openai.com/v1
CUSTOM_API_MODEL=gpt-4o-mini
```

Other OpenAI-Compatible Providers

```env
CUSTOM_API_KEY=your_api_key
CUSTOM_API_BASE_URL=https://your-provider.com/v1
CUSTOM_API_MODEL=your-model
```

---

▶️ Run the Bot

Start the bot:

```bash
python bot.py
```

On the first run, Telegram will ask you to authenticate.
You will need to enter:

1. Your phone number
2. Telegram verification code
3. Two-factor authentication password, if enabled

After successful authentication, the bot will create market_session.session.
You normally won't need to authenticate again on subsequent runs.

---

🖥️ Production Deployment

For a Linux server or VPS, you can run the bot as a systemd service.

1. Copy the service file:

```bash
sudo cp marketbot.service /etc/systemd/system/
```

2. Reload systemd:

```bash
sudo systemctl daemon-reload
```

3. Enable the bot:

```bash
sudo systemctl enable marketbot
```

4. Start the bot:

```bash
sudo systemctl start marketbot
```

5. Check status:

```bash
sudo systemctl status marketbot
```

6. View live logs:

```bash
journalctl -u marketbot -f
```

Or:

```bash
tail -f market_bot.log
```

---

🔧 Configuration Reference

Variable Description Example
TELEGRAM_API_ID Telegram API ID 12345678
TELEGRAM_API_HASH Telegram API hash your_api_hash
TARGET_CHANNEL Telegram channel @your_channel
CRYPTO_THRESHOLD_PCT Crypto alert threshold 5.0
METALS_THRESHOLD_PCT Metals alert threshold 2.0
COOLDOWN_HOURS Alert cooldown 4
CUSTOM_API_KEY AI API key your_api_key
CUSTOM_API_BASE_URL AI API endpoint https://api.deepseek.com/v1
CUSTOM_API_MODEL AI model deepseek-chat

---

📊 Default Volatility Triggers

Asset Trigger
BTC ≥ 5%
ETH ≥ 5%
SOL ≥ 5%
Gold ≥ 2%
Silver ≥ 2%

You can change these values in .env:

```env
CRYPTO_THRESHOLD_PCT=3.0
METALS_THRESHOLD_PCT=1.5
```

---

🔄 How It Works

```
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
```

---

📡 Data Sources

Cryptocurrency – Market prices are retrieved from the Binance public Spot API. No Binance API key is required for public market data.

Precious Metals – Gold and Silver prices are retrieved through publicly available Stooq / Yahoo market data feeds.

News – Relevant breaking news is collected through Google News RSS, focused on macroeconomic and market-moving events.

---

🛡️ Anti-Spam Protection

The bot includes a configurable cooldown period.

Example:

```env
COOLDOWN_HOURS=4
```

If an asset triggers an alert, the bot won't repeatedly send duplicate alerts during the cooldown period.

---

🔒 Security

Never commit sensitive files to GitHub.

Recommended .gitignore:

```
.env
*.session
__pycache__/
*.pyc
venv/
market_bot.log
```

Keep the following private:

· Telegram API credentials
· AI API keys
· .env
· Telegram session files

---

🐛 Troubleshooting

Check Python Dependencies

```bash
pip install -r requirements.txt
```

Check Telegram Session

```bash
ls -la *.session
```

Check systemd Status

```bash
sudo systemctl status marketbot
```

Check systemd Logs

```bash
sudo journalctl -u marketbot -n 100 --no-pager
```

Check .env

```bash
ls -la .env
```

---

📜 License

MIT License.

Free to use, modify, and distribute.