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

CRYPTO_THRESHOLD_PCT = float(os.getenv("CRYPTO_THRESHOLD_PCT", 5.0))
METALS_THRESHOLD_PCT = float(os.getenv("METALS_THRESHOLD_PCT", 2.0))
COOLDOWN_HOURS = float(os.getenv("COOLDOWN_HOURS", 4))

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
    return sqlite3.connect(DB_FILE, timeout=15.0)

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS price_history 
                 (symbol TEXT, price REAL, timestamp REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS alerts_sent 
                 (symbol TEXT, pct_change REAL, price REAL, timestamp REAL)''')
    c.execute('''CREATE INDEX IF NOT EXISTS idx_price_ts ON price_history(timestamp)''')
    c.execute('''CREATE INDEX IF NOT EXISTS idx_alerts_ts ON alerts_sent(timestamp)''')
    conn.commit()
    conn.close()

# ==========================================
# DATA INGESTION & NEWS PARSERS
# ==========================================
def fetch_crypto_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        res = requests.get(url, timeout=5).json()
        return float(res["price"])
    except Exception as e:
        logging.warning(f"Error fetching {symbol}: {e}")
        return None

def fetch_metal_price(symbol):
    try:
        ticker = "XAUUSD" if symbol == "XAUUSD" else "XAGUSD"
        url = f"https://stooq.com/q/l/?s={ticker.lower()}&f=sd2t2ohlc&h&e=csv"
        res = requests.get(url, timeout=5)
        lines = res.text.strip().split("\n")
        if len(lines) > 1:
            val = float(lines[1].split(",")[-1])
            if val > 0: return val
    except Exception as e:
        logging.warning(f"Error fetching metal {symbol}: {e}")
    return None

def get_current_price(symbol, asset_type):
    return fetch_crypto_price(symbol) if asset_type == "crypto" else fetch_metal_price(symbol)

def fetch_market_breaking_news(query_keyword):
    macro_catalysts = "(Trump OR Fed OR Powell OR Treasury OR SEC OR inflation OR CPI OR War OR ETF OR liquidated OR interest)"
    query = f"when:4h ({query_keyword}) AND {macro_catalysts}"
    rss_url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"
    
    articles = []
    try:
        resp = requests.get(rss_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            for item in root.findall('.//item')[:5]:
                title = item.find('title').text or ""
                desc = item.find('description').text or ""
                clean_desc = re.sub(r'<[^>]+>', '', desc)
                articles.append(f"• {std_html.unescape(title)}: {std_html.unescape(clean_desc)[:120]}")
    except Exception as e:
        logging.warning(f"News fetch error for {query_keyword}: {e}")
        
    return "\n".join(articles) if articles else "عامل تکنیکال، جریان ورود/خروج ETF یا لیکوئیدیشن مشتقات (بدون بیانیه مستقل جدید)"

# ==========================================
# AI SYNTHESIS ENGINE
# ==========================================
def generate_ai_analysis(asset_name, pct_change, current_price, news_context):
    direction = "صعودی (پامپ)" if pct_change > 0 else "نزولی (دامپ / ریزش)"
    
    prompt = f"""شما یک تحلیل‌گر ارشد اقتصاد کلان و بازارهای مالی هستید.
دارایی: {asset_name}
نوسان اخیر: {pct_change:+.2f}% ({direction})
قیمت فعلی: {current_price:,.2f} دلار

اخبار و عوامل لحظه‌ای اخیر (مواضع ترامپ، فدرال رزرو، خزانه‌داری آمریکا یا شاخص‌های کلان):
{news_context}

یک گزارش تحلیلی ساختاریافته به زبان فارسی در ۴ بخش آماده کن:
1. 🚨 <b>علت و محرک اصلی نوسان</b> (توضیح کوتاه اینکه دقیقا چه خبر یا عاملی محرک این حرکت شد).
2. 📌 <b>جزئیات کلیدی خبر</b> (نکات تکمیلی در ۱ الی ۲ بولت‌پوینت کوتاه).
3. 🔮 <b>پیش‌بینی و سناریوی بعدی (چه خواهد شد؟)</b> (بررسی ۲ سناریو: اگر مومنتوم حفظ شود چه سطحی هدف است، و در صورت برگشت چه حمایتی کلیدی است).
4. ⚠️ <b>نکته مدیریت ریسک</b>.

پاسخ را بدون مقدمه و متن اضافه با تگ‌های HTML معتبر بنویس."""

    if CUSTOM_API_KEY:
        try:
            endpoint = f"{CUSTOM_API_BASE_URL.rstrip('/')}/chat/completions"
            headers = {"Authorization": f"Bearer {CUSTOM_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": CUSTOM_API_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
            resp = requests.post(endpoint, json=payload, headers=headers, timeout=15)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logging.warning(f"Custom AI failed: {e}. Falling back to keyless pool...")

    # Keyless Fallback Engine
    try:
        url = "https://text.pollinations.ai/"
        payload = {"messages": [{"role": "user", "content": prompt}], "model": "mistral"}
        r = requests.post(url, json=payload, timeout=12)
        if r.status_code == 200:
            return r.text.strip()
    except Exception as e:
        logging.error(f"Fallback AI failed: {e}")
        
    return f"⚠️ نوسان شدید {pct_change:+.2f}% در {asset_name}.\nقیمت فعلی: {current_price:,.2f}$"

# ==========================================
# VOLATILITY MONITOR & BROADCASTER
# ==========================================
async def check_volatility(client):
    conn = get_db()
    c = conn.cursor()
    now_ts = datetime.now().timestamp()
    one_day_ago = (datetime.now() - timedelta(hours=24)).timestamp()
    
    for symbol, meta in TRACKED_ASSETS.items():
        current_price = await asyncio.to_thread(get_current_price, symbol, meta["type"])
        if not current_price:
            continue
            
        c.execute("INSERT INTO price_history (symbol, price, timestamp) VALUES (?, ?, ?)", 
                  (symbol, current_price, now_ts))
        
        row = c.execute("""SELECT price FROM price_history 
                           WHERE symbol=? AND timestamp >= ? 
                           ORDER BY timestamp ASC LIMIT 1""", (symbol, one_day_ago)).fetchone()
        
        if row:
            base_price = row[0]
            pct_change = ((current_price - base_price) / base_price) * 100
            threshold = CRYPTO_THRESHOLD_PCT if meta["type"] == "crypto" else METALS_THRESHOLD_PCT
            
            if abs(pct_change) >= threshold:
                cooldown_cutoff = (datetime.now() - timedelta(hours=COOLDOWN_HOURS)).timestamp()
                recent_alert = c.execute("""SELECT 1 FROM alerts_sent 
                                           WHERE symbol=? AND timestamp > ?""", 
                                         (symbol, cooldown_cutoff)).fetchone()
                
                if not recent_alert:
                    logging.info(f"Threshold reached: {symbol} shifted {pct_change:+.2f}%")
                    news_context = await asyncio.to_thread(fetch_market_breaking_news, meta["search_term"])
                    analysis = await asyncio.to_thread(generate_ai_analysis, meta["name"], pct_change, current_price, news_context)
                    
                    header_icon = "🟢 📈" if pct_change > 0 else "🔴 📉"
                    final_post = (
                        f"{header_icon} <b>هشدار نوسان شدید در {meta['name']}</b>\n"
                        f"تغییر ۲۴ ساعته: <b>{pct_change:+.2f}%</b> | قیمت: <b>{current_price:,.2f}$</b>\n\n"
                        f"{analysis}"
                        f"{BOT_SIGNATURE}"
                    )
                    
                    try:
                        await client.send_message(TARGET_CHANNEL, final_post, parse_mode='html')
                        logging.info(f"Posted alert for {symbol} to {TARGET_CHANNEL}")
                        c.execute("INSERT INTO alerts_sent (symbol, pct_change, price, timestamp) VALUES (?, ?, ?, ?)",
                                  (symbol, pct_change, current_price, now_ts))
                        conn.commit()
                    except Exception as tg_err:
                        logging.error(f"Telegram broadcast error: {tg_err}")

    # Remove history entries older than 48 hours
    c.execute("DELETE FROM price_history WHERE timestamp < ?", ((datetime.now() - timedelta(days=2)).timestamp(),))
    conn.commit()
    conn.close()

# ==========================================
# MAIN EXECUTION LOOP
# ==========================================
async def main():
    if not API_ID or not API_HASH or not TARGET_CHANNEL:
        raise ValueError("Missing critical configuration. Run `python setup.py` first.")
        
    init_db()
    client = TelegramClient('market_session', API_ID, API_HASH)
    await client.start()
    logging.info("Market Volatility & Macro News Bot online. Monitoring assets...")
    
    while True:
        try:
            await check_volatility(client)
        except Exception as e:
            logging.error(f"Execution loop exception: {e}")
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
