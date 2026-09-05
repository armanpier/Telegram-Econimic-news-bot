#!/usr/bin/env bash
set -e

clear
echo "======================================================"
echo "   🚀 Telegram Market News Bot - Automated Setup      "
echo "======================================================"
echo ""

# 1. Verify Python & Tools
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 is not installed. Run: sudo apt update && sudo apt install -y python3 python3-venv python3-pip"
    exit 1
fi

# 2. Automated Virtual Environment & Dependency Installation
echo "📦 Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv || { echo "❌ Could not create venv. Run: sudo apt install -y python3-venv"; exit 1; }
fi

source venv/bin/activate
echo "📥 Installing required Python dependencies..."
pip install --upgrade pip >/dev/null 2>&1
pip install -r requirements.txt

# 3. Interactive Configuration Prompts
echo ""
echo "--- 1. Telegram API Credentials ---"
echo "Obtain these from: https://my.telegram.org"

while true; do
    read -p "Enter Telegram API ID: " TELEGRAM_API_ID
    [[ -n "$TELEGRAM_API_ID" ]] && break
    echo "  ❌ API ID is required."
done

while true; do
    read -p "Enter Telegram API Hash: " TELEGRAM_API_HASH
    [[ -n "$TELEGRAM_API_HASH" ]] && break
    echo "  ❌ API Hash is required."
done

while true; do
    read -p "Enter Target Channel (@username or channel ID): " TARGET_CHANNEL
    [[ -n "$TARGET_CHANNEL" ]] && break
    echo "  ❌ Target channel is required."
done

if [[ ! "$TARGET_CHANNEL" =~ ^@ ]] && [[ ! "$TARGET_CHANNEL" =~ ^-100 ]]; then
    TARGET_CHANNEL="@$TARGET_CHANNEL"
fi

echo ""
echo "--- 2. Market Alert Thresholds ---"
read -p "Crypto 24h Volatility Trigger % [default: 5.0]: " CRYPTO_THRESHOLD
CRYPTO_THRESHOLD=${CRYPTO_THRESHOLD:-5.0}

read -p "Gold/Silver 24h Volatility Trigger % [default: 2.0]: " METALS_THRESHOLD
METALS_THRESHOLD=${METALS_THRESHOLD:-2.0}

read -p "Cooldown window per asset in hours [default: 3]: " COOLDOWN_HOURS
COOLDOWN_HOURS=${COOLDOWN_HOURS:-3}

echo ""
echo "--- 3. AI Analysis Engine ---"
echo "Select AI provider for news root-cause analysis:"
echo "  [1] Free Keyless AI Pool (Default - No API key needed)"
echo "  [2] DeepSeek API (Recommended)"
echo "  [3] OpenAI / Groq / Custom OpenAI-compatible endpoint"
read -p "Select option [1-3, default: 1]: " AI_CHOICE
AI_CHOICE=${AI_CHOICE:-1}

CUSTOM_API_KEY=""
CUSTOM_API_BASE_URL="https://api.deepseek.com/v1"
CUSTOM_API_MODEL="deepseek-chat"

if [ "$AI_CHOICE" == "2" ]; then
    read -p "Enter DeepSeek API Key: " CUSTOM_API_KEY
    CUSTOM_API_BASE_URL="https://api.deepseek.com/v1"
    CUSTOM_API_MODEL="deepseek-chat"
elif [ "$AI_CHOICE" == "3" ]; then
    read -p "Enter API Key: " CUSTOM_API_KEY
    read -p "Enter Base URL [default: https://api.openai.com/v1]: " CUSTOM_API_BASE_URL
    CUSTOM_API_BASE_URL=${CUSTOM_API_BASE_URL:-https://api.openai.com/v1}
    read -p "Enter Model Name [default: gpt-4o-mini]: " CUSTOM_API_MODEL
    CUSTOM_API_MODEL=${CUSTOM_API_MODEL:-gpt-4o-mini}
fi

# 4. Write .env File
echo ""
echo "📝 Writing parameters to .env..."
cat <<EOF > .env
TELEGRAM_API_ID=${TELEGRAM_API_ID}
TELEGRAM_API_HASH=${TELEGRAM_API_HASH}
TARGET_CHANNEL=${TARGET_CHANNEL}

CRYPTO_THRESHOLD_PCT=${CRYPTO_THRESHOLD}
METALS_THRESHOLD_PCT=${METALS_THRESHOLD}
COOLDOWN_HOURS=${COOLDOWN_HOURS}

CUSTOM_API_KEY=${CUSTOM_API_KEY}
CUSTOM_API_BASE_URL=${CUSTOM_API_BASE_URL}
CUSTOM_API_MODEL=${CUSTOM_API_MODEL}
EOF
echo "✅ .env configuration generated."

# 5. Telegram Session Login (Explicit .env path avoids Python 3.12 stdin frame bug)
echo ""
echo "--- 4. Telegram Account Authentication ---"
echo "Logging in to generate your Telegram session..."
python3 - << 'PY_AUTH'
import os
from telethon.sync import TelegramClient
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

with TelegramClient('market_session', api_id, api_hash) as client:
    user = client.get_me()
    print(f"\n✅ Authenticated as: {user.first_name} (@{user.username})")
PY_AUTH

# 6. Linux Service Deployment
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo ""
    echo "--- 5. Background Service Deployment ---"
    read -p "Register and launch 24/7 systemd background service? (y/n) [default: y]: " INSTALL_SERVICE
    INSTALL_SERVICE=${INSTALL_SERVICE:-y}

    if [[ "$INSTALL_SERVICE" =~ ^[Yy]$ ]]; then
        CURRENT_USER=$(whoami)
        CURRENT_DIR=$(pwd)
        PYTHON_EXEC="${CURRENT_DIR}/venv/bin/python"
        SERVICE_PATH="/etc/systemd/system/marketbot.service"

        echo "⚙️ Creating /etc/systemd/system/marketbot.service..."
        sudo bash -c "cat <<EOF > $SERVICE_PATH
[Unit]
Description=Market Volatility & Macro News Telegram Bot
After=network.target

[Service]
Type=simple
User=${CURRENT_USER}
WorkingDirectory=${CURRENT_DIR}
ExecStart=${PYTHON_EXEC} bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF"

        sudo systemctl daemon-reload
        sudo systemctl enable --now marketbot
        echo "✅ Service registered and running in the background."
    fi
fi

echo ""
echo "======================================================"
echo "  🎉 Installation Complete!                           "
echo "  To view live logs, run:                             "
echo "      journalctl -u marketbot -f                      "
echo "======================================================"
