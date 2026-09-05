import os
import re
import time
import sqlite3
import logging
import asyncio
import html as std_html
import xml.etree.ElementTree as ET
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

# ==========================================
# CONFIGURATION
# ==========================================
API_ID = int(os.getenv("TELEGRAM_API_ID", 0))
API_HASH = os.getenv("TELEGRAM_API_HASH", "")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL", "")

# Dual-Window Triggers
CRYPTO_24H_THRESHOLD = float(os.getenv("CRYPTO_THRESHOLD_PCT", 5.0))
CRYPTO_1H_THRESHOLD = 3.0    # 1-hour flash move
METALS_24H_THRESHOLD = float(os.getenv("METALS_THRESHOLD_PCT", 2.0))
METALS_1H_THRESHOLD = 1.2    # 1-hour flash move
COOLDOWN_HOURS = float(os.getenv("COOLDOWN_HOURS", 3))

CUSTOM_API_KEY = os.getenv("CUSTOM_API_KEY", "").strip()
CUSTOM_API_BASE_URL = os.getenv("CUSTOM_API_BASE_URL", "https://api.deepseek.com/v1").strip()
CUSTOM_API_MODEL = os.getenv("CUSTOM_API_MODEL", "deepseek-chat").strip()

BOT_SIGNATURE = "\n\n@khabaravalai | تحلیل هوش مصنوعی بازار"
DB_FILE = "market_bot.db"

TRACKED_ASSETS = {
    "BTCUSDT": {"name": "بیت‌کوین (BTC)", "type": "crypto", "search_term": "Bitcoin OR BTC"},
    "ETHUSDT": {"name": "اتریوم (ETH)", "type": "crypto", "search_term": "Ethereum OR ETH"},
    "SOLUSDT": {"name": "سولانا (SOL)", "type": "crypto", "search_term": "Solana OR SOL"},
    "XAUUSD":  {"name": "انس جهانی طلا (Gold)", "type": "metal", "search_term": "Gold OR XAU OR Bullion"},
    "XAGUSD":  {"name": "نقره جهانی (Silver)", "type": "metal", "search_term": "Silver OR XAG"}
}

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler("market_bot.log"), logging.StreamHandler()]
)

# ==========================================
# DATABASE INITIALIZATION
# ==========================================
def get_db():
    return sqlite3.connect(DB_FILE, timeout=20.0)

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS price_history 
                        (symbol TEXT, price REAL, timestamp REAL)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS alerts_sent 
                        (symbol TEXT, window TEXT, pct_change REAL, price REAL, timestamp REAL)''')
        conn.execute('''CREATE INDEX IF NOT EXISTS idx_price_lookup ON price_history(symbol, timestamp)''')
        conn.execute('''CREATE INDEX IF NOT EXISTS idx_alerts_lookup ON alerts_sent(symbol, timestamp)''')

# ==========================================
# ROBUST DATA FETCHERS
# ==========================================
def fetch_crypto_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        res = requests.get(url, timeout=6).json()
        return float(res["price"])
    except Exception as e:
        logging.warning(f"Binance fetch error ({symbol}): {e}")
        return None

def fetch_metal_price(symbol):
    # Primary: Stooq CSV feed
    try:
        ticker = "xauusd" if symbol == "XAUUSD" else "xagusd"
        url = f"https://stooq.com/q/l/?s={ticker}&f=sd2t2ohlc&h&e=csv"
        res = requests.get(url, timeout=6)
        lines = res.text.strip().split("\n")
        if len(lines) > 1:
            raw_val = lines[1].split(",")[-1].strip()
            if raw_val and raw_val != "N/D":
                return float(raw_val)
    except Exception:
        pass

    # Fallback for Gold: Binance PAXGUSDT (1:1 physical gold backing)
    if symbol == "XAUUSD":
        try:
            res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT", timeout=6).json()
            return float(res["price"])
        except Exception:
            pass

    return None

def get_current_price(symbol, asset_type):
    return fetch_crypto_price(symbol) if asset_type == "crypto" else fetch_metal_price(symbol)

# ==========================================
# TARGETED NEWS AGGREGATOR
# ==========================================
def fetch_market_breaking_news(query_keyword):
    macro_catalysts = "(Trump OR Fed OR Powell OR Treasury OR SEC OR inflation OR CPI OR War OR ETF OR liquidated OR tariffs)"
    query = f"when:4h ({query_keyword}) AND {macro_catalysts}"
    rss_url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"
    
    articles = []
    try:
        resp = requests.get(rss_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            for item in root.findall('.//item')[:4]:
                title = item.find('title').text or ""
                desc = item.find('description').text or ""
                clean_desc = re.sub(r'<[^>]+>', '', desc)
                clean_title = std_html.unescape(title).strip()
                clean_desc = std_html.unescape(clean_desc).strip()
                articles.append(f"• {clean_title}: {clean_desc[:120]}")
    except Exception as e:
        logging.warning(f"News fetch error for {query_keyword}: {e}")
        
    return "\n".join(articles) if articles else "حرکت شدید بر اثر لیکوئیدیشن مشتقه یا مومنتوم تکنیکال (بیانیه خبری مجزایی ثبت نشد)"

# ==========================================
# AI SYNTHESIS ENGINE
# ==========================================
def generate_ai_analysis(asset_name, window_label, pct_change, current_price, news_context):
    direction = "صعودی (پامپ)" if pct_change > 0 else "نزولی (دامپ / ریزش)"
    
    prompt = f"""شما یک تحلیل‌گر ارشد بازارهای مالی و اقتصاد کلان هستید.
دارایی: {asset_name}
بازه نوسان: {window_label}
درصد تغییر: {pct_change:+.2f}% ({direction})
قیمت فعلی: {current_price:,.2f} دلار

اخبار و شواهد لحظه‌ای (شامل مواضع ترامپ، فدرال رزرو، خزانه‌داری آمریکا یا لیکوئیدیشن):
{news_context}

یک گزارش تحلیلی ساختاریافته به فارسی در ۴ بخش آماده کن:
1. 🚨 <b>علت و محرک اصلی نوسان</b> (توضیح مستقیم اینکه چه خبر یا عاملی این حرکت را ایجاد کرد).
2. 📌 <b>جزئیات کلیدی خبر</b> (۱ الی ۲ نکته مهم).
3. 🔮 <b>پیش‌بینی و سناریوی بعدی (چه خواهد شد؟)</b> (بررسی ۲ سناریو: تارگت بعدی در صورت ادامه مومنتوم، و حمایت/مقاومت کلیدی در صورت برگشت).
4. ⚠️ <b>نکته مدیریت ریسک</b>.

پاسخ را بدون مقدمه اضافی با تگ‌های HTML تمیز (فقط b و i) بنویس."""

    if CUSTOM_API_KEY:
        try:
            endpoint = f"{CUSTOM_API_BASE_URL.rstrip('/')}/chat/completions"
            headers = {"Authorization": f"Bearer {CUSTOM_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": CUSTOM_API_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.25
            }
            resp = requests.post(endpoint, json=payload, headers=headers, timeout=16)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logging.warning(f"Custom AI failed: {e}. Trying fallback pool...")

    # Free Pollinations AI Pool
    try:
        url = "https://text.pollinations.ai/"
        payload = {"messages": [{"role": "user", "content": prompt}], "model": "mistral"}
        r = requests.post(url, json=payload, timeout=14)
        if r.status_code == 200 and r.text.strip():
            return r.text.strip()
    except Exception as e:
        logging.error(f"Fallback AI failed: {e}")
        
    return f"⚠️ نوسان شدید {pct_change:+.2f}% در {asset_name} طی {window_label}.\nقیمت فعلی: {current_price:,.2f}$"

# ==========================================
# VOLATILITY ENGINE (DUAL-WINDOW)
# ==========================================
def get_historical_baseline(symbol, target_seconds_ago, max_tolerance_seconds):
    target_ts = datetime.now().timestamp() - target_seconds_ago
    with get_db() as conn:
        row = conn.execute("""SELECT price, timestamp FROM price_history 
                              WHERE symbol=? AND timestamp <= ? 
                              ORDER BY timestamp DESC LIMIT 1""", (symbol, target_ts)).fetchone()
        if row and abs(row[1] - target_ts) <= max_tolerance_seconds:
            return row[0]
    return None

def check_cooldown(symbol):
    cooldown_cutoff = (datetime.now() - timedelta(hours=COOLDOWN_HOURS)).timestamp()
    with get_db() as conn:
        row = conn.execute("SELECT 1 FROM alerts_sent WHERE symbol=? AND timestamp > ?", 
                           (symbol, cooldown_cutoff)).fetchone()
        return bool(row)

async def check_volatility(client):
    now_ts = datetime.now().timestamp()
    
    for symbol, meta in TRACKED_ASSETS.items():
        current_price = await asyncio.to_thread(get_current_price, symbol, meta["type"])
        if not current_price:
            continue
            
        with get_db() as conn:
            conn.execute("INSERT INTO price_history (symbol, price, timestamp) VALUES (?, ?, ?)", 
                         (symbol, current_price, now_ts))

        if check_cooldown(symbol):
            continue

        base_1h = get_historical_baseline(symbol, target_seconds_ago=3600, max_tolerance_seconds=1800)
        base_24h = get_historical_baseline(symbol, target_seconds_ago=86400, max_tolerance_seconds=7200)

        alert_triggered = False
        window_label = ""
        pct_change = 0.0

        # Check 1: Rapid 1-Hour Flash Move
        if base_1h:
            chg_1h = ((current_price - base_1h) / base_1h) * 100
            thresh_1h = CRYPTO_1H_THRESHOLD if meta["type"] == "crypto" else METALS_1H_THRESHOLD
            if abs(chg_1h) >= thresh_1h:
                alert_triggered = True
                window_label = "۱ ساعت گذشته (نوسان فوری)"
                pct_change = chg_1h

        # Check 2: 24-Hour Macro Trend Move
        if not alert_triggered and base_24h:
            chg_24h = ((current_price - base_24h) / base_24h) * 100
            thresh_24h = CRYPTO_24H_THRESHOLD if meta["type"] == "crypto" else METALS_24H_THRESHOLD
            if abs(chg_24h) >= thresh_24h:
                alert_triggered = True
                window_label = "۲۴ ساعت گذشته"
                pct_change = chg_24h

        if alert_triggered:
            logging.info(f"🚨 Volatility Alert: {symbol} shifted {pct_change:+.2f}% over {window_label}")
            news_context = await asyncio.to_thread(fetch_market_breaking_news, meta["search_term"])
            analysis = await asyncio.to_thread(generate_ai_analysis, meta["name"], window_label, pct_change, current_price, news_context)
            
            header_icon = "🟢 📈" if pct_change > 0 else "🔴 📉"
            final_post = (
                f"{header_icon} <b>هشدار نوسان شدید در {meta['name']}</b>\n"
                f"تغییر: <b>{pct_change:+.2f}%</b> ({window_label})\n"
                f"قیمت فعلی: <b>{current_price:,.2f}$</b>\n\n"
                f"{analysis}"
                f"{BOT_SIGNATURE}"
            )
            
            # Safe Telegram Dispatch with Plaintext Fallback
            try:
                await client.send_message(TARGET_CHANNEL, final_post, parse_mode='html')
                logging.info(f"Alert broadcasted for {symbol}")
            except Exception as html_err:
                logging.warning(f"HTML parse failed ({html_err}). Sending plain text fallback.")
                plain_text = re.sub(r'<[^>]+>', '', final_post)
                await client.send_message(TARGET_CHANNEL, plain_text)

            with get_db() as conn:
                conn.execute("INSERT INTO alerts_sent (symbol, window, pct_change, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                             (symbol, window_label, pct_change, current_price, now_ts))

    # Prune history older than 48 hours
    with get_db() as conn:
        conn.execute("DELETE FROM price_history WHERE timestamp < ?", ((datetime.now() - timedelta(days=2)).timestamp(),))

# ==========================================
# MAIN LOOP
# ==========================================
async def main():
    if not API_ID or not API_HASH or not TARGET_CHANNEL:
        raise ValueError("Missing critical configuration in .env. Run `python setup.py` first.")
        
    init_db()
    client = TelegramClient('market_session', API_ID, API_HASH)
    await client.start()
    logging.info("Market Volatility & Macro Bot online. Monitoring feeds...")
    
    while True:
        try:
            await check_volatility(client)
        except Exception as e:
            logging.error(f"Execution loop error: {e}")
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
