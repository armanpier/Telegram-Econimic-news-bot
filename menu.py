import os
import re
import sys
import subprocess
import requests

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

def get_env_val(key, default=""):
    if not os.path.exists(ENV_PATH):
        return default
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith(f"{key}="):
                return line.strip().split("=", 1)[1].strip()
    return default

def set_env_val(key, val):
    lines = []
    found = False
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={val}\n")
            found = True
        else:
            new_lines.append(line)

    if not found:
        new_lines.append(f"{key}={val}\n")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def prompt(text, default=""):
    prompt_str = f"{text} [{default}]: " if default else f"{text}: "
    val = input(prompt_str).strip()
    return val if val else default

def restart_service():
    print("\n🔄 Restarting marketbot service to apply changes...")
    subprocess.run(["sudo", "systemctl", "restart", "marketbot"])
    print("✅ Service restarted.")

def config_ai():
    print("\n==========================================")
    print("         🤖 AI ENGINE CONFIGURATION        ")
    print("==========================================")
    current_key = get_env_val("CUSTOM_API_KEY", "")
    current_url = get_env_val("CUSTOM_API_BASE_URL", "https://api.deepseek.com/v1")
    current_model = get_env_val("CUSTOM_API_MODEL", "deepseek-chat")

    if not current_key:
        active_engine = "Free Keyless Fallback Pool"
    elif "deepseek" in current_url:
        active_engine = f"DeepSeek ({current_model})"
    else:
        active_engine = f"Custom/OpenAI ({current_model})"

    print(f"Current Engine : {active_engine}")
    print(f"Current Key    : {'*' * 8 + current_key[-4:] if current_key else 'None'}")
    print(f"Current Base URL: {current_url}")
    print(f"Current Model  : {current_model}")
    print("------------------------------------------")
    print(" [1] Switch to Free Keyless Pool (No key required)")
    print(" [2] Configure DeepSeek API (Recommended)")
    print(" [3] Configure OpenAI / Groq / Custom Endpoint")
    print(" [0] Cancel")
    
    choice = input("\nSelect an option [0-3]: ").strip()
    if choice == "1":
        set_env_val("CUSTOM_API_KEY", "")
        print("✅ Switched to Free Keyless AI Pool.")
        restart_service()
    elif choice == "2":
        key = prompt("Enter DeepSeek API Key", current_key if current_key else "")
        set_env_val("CUSTOM_API_KEY", key)
        set_env_val("CUSTOM_API_BASE_URL", "https://api.deepseek.com/v1")
        set_env_val("CUSTOM_API_MODEL", "deepseek-chat")
        print("✅ DeepSeek API configured.")
        restart_service()
    elif choice == "3":
        key = prompt("Enter API Key", current_key if current_key else "")
        url = prompt("Enter Base URL", current_url)
        model = prompt("Enter Model Name", current_model)
        set_env_val("CUSTOM_API_KEY", key)
        set_env_val("CUSTOM_API_BASE_URL", url)
        set_env_val("CUSTOM_API_MODEL", model)
        print("✅ Custom AI Provider configured.")
        restart_service()

def config_thresholds():
    print("\n==========================================")
    print("      📊 ALERT THRESHOLDS & TIMERS        ")
    print("==========================================")
    curr_crypto = get_env_val("CRYPTO_THRESHOLD_PCT", "5.0")
    curr_metal = get_env_val("METALS_THRESHOLD_PCT", "2.0")
    curr_cooldown = get_env_val("COOLDOWN_HOURS", "3")

    print(f"Current Crypto 24h Trigger : ±{curr_crypto}%")
    print(f"Current Gold/Silver Trigger: ±{curr_metal}%")
    print(f"Current Asset Cooldown     : {curr_cooldown} hours")
    print("------------------------------------------")

    new_crypto = prompt("Enter Crypto 24h Trigger %", curr_crypto)
    new_metal = prompt("Enter Gold/Silver 24h Trigger %", curr_metal)
    new_cooldown = prompt("Enter Cooldown in hours", curr_cooldown)

    set_env_val("CRYPTO_THRESHOLD_PCT", new_crypto)
    set_env_val("METALS_THRESHOLD_PCT", new_metal)
    set_env_val("COOLDOWN_HOURS", new_cooldown)
    print("✅ Thresholds updated.")
    restart_service()

def config_target_channel():
    print("\n==========================================")
    print("         📢 TARGET TELEGRAM CHANNEL       ")
    print("==========================================")
    curr_ch = get_env_val("TARGET_CHANNEL", "")
    print(f"Current Channel: {curr_ch}")
    new_ch = prompt("Enter new target channel (@username or ID)", curr_ch)
    if new_ch and not new_ch.startswith("@") and not new_ch.startswith("-100"):
        new_ch = "@" + new_ch
    set_env_val("TARGET_CHANNEL", new_ch)
    print("✅ Target channel updated.")
    restart_service()

def interactive_menu():
    while True:
        key = get_env_val("CUSTOM_API_KEY", "")
        model = get_env_val("CUSTOM_API_MODEL", "deepseek-chat")
        engine_name = f"Custom ({model})" if key else "Free AI Pool"
        crypto_th = get_env_val("CRYPTO_THRESHOLD_PCT", "5.0")
        target_ch = get_env_val("TARGET_CHANNEL", "Not set")

        print("\n==============================================")
        print("          📈 ECOBOT CONTROL DASHBOARD          ")
        print("==============================================")
        print(f" Target Channel : {target_ch}")
        print(f" Active AI      : {engine_name}")
        print(f" Crypto Trigger : ±{crypto_th}%")
        print("----------------------------------------------")
        print(" [1] 📜 View Live Stream Logs")
        print(" [2] 🔍 Check Service Health (Status)")
        print(" [3] 🔄 Restart Bot Daemon")
        print(" [4] 🛑 Stop Service")
        print(" [5] ▶️  Start Service")
        print("----------------------------------------------")
        print(" [6] 🤖 Change AI Engine & API Key")
        print(" [7] 📊 Change Alert Thresholds & Cooldown")
        print(" [8] 📢 Change Target Channel")
        print(" [0] ❌ Exit")
        print("==============================================")
        
        choice = input("Select an option [0-8]: ").strip()
        if choice == "1":
            try:
                subprocess.run(["journalctl", "-u", "marketbot", "-f"])
            except KeyboardInterrupt:
                pass
        elif choice == "2":
            subprocess.run(["sudo", "systemctl", "status", "marketbot"])
        elif choice == "3":
            restart_service()
        elif choice == "4":
            subprocess.run(["sudo", "systemctl", "stop", "marketbot"])
            print("🛑 Service stopped.")
        elif choice == "5":
            subprocess.run(["sudo", "systemctl", "start", "marketbot"])
            print("▶️ Service started.")
        elif choice == "6":
            config_ai()
        elif choice == "7":
            config_thresholds()
        elif choice == "8":
            config_target_channel()
        elif choice == "0":
            break

if __name__ == "__main__":
    interactive_menu()
