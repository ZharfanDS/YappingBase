import os
import time
import random
import requests
import datetime
import schedule
from google import genai
from dotenv import load_dotenv

load_dotenv()

# --- 1. KONFIGURASI KREDENSIAL ---
WARPCAST_TOKEN = os.getenv("WARPCAST_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- 2. INISIALISASI CLIENT ---
# Menggunakan SDK google-genai terbaru (v1.0+)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

def generate_base_yap():
    """Menghasilkan konten yapping tentang Base menggunakan Gemini 2.0 Flash"""
    topics = [
        "current trends in the Base Network ecosystem",
        "why Base App is the best gateway for onchain users",
        "the future of Layer 2 solutions focusing on Base",
        "witty insights about Base Network decentralization",
        "creative take on the 'Build on Base' culture"
    ]
    
    selected_topic = random.choice(topics)
    
    prompt = (
        f"Role: You are a creative member of the Base community. "
        f"Task: Write a high-quality post about: {selected_topic}. "
        "Guidelines: "
        "- Use casual 'crypto degen' or 'onchain' language. "
        #"- MUST include these hashtags: #BaseApp #Base #BaseNetwork. "
        "- Keep the total length under 145 characters. "
        "- Tone: Positive, insightful, and trendy. "
        "- No quotes at the beginning and end. "
        "Language: English."
    )
    
    try:
        # Panggilan model terbaru
        response = ai_client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()[:150]
    except Exception as e:
        print(f"[{datetime.datetime.now()}] AI Error: {e}")
        return "Building on Base is just different. The vibe is unmatched. 🔵 #BaseApp #Base #BaseNetwork"

def kirim_cast():
    """Eksekusi pengiriman postingan ke Warpcast dengan Random Delay"""
    
    # Random delay 1-15 menit (60 - 900 detik)
    delay_detik = random.randint(60, 900)
    menit = delay_detik // 60
    print(f"[{datetime.datetime.now()}] Jadwal tercapai. Menunggu {menit} menit agar terlihat natural...")
    time.sleep(delay_detik)

    print(f"[{datetime.datetime.now()}] Memulai proses kirim cast...")
    pesan = generate_base_yap()
    
    # Endpoint internal Warpcast (Unofficial method)
    url = "https://client.warpcast.com/v2/casts"
    headers = {
        "authorization": f"Bearer {WARPCAST_TOKEN}",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    payload = {"text": pesan}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code in [200, 201]:
            print(f"[{datetime.datetime.now()}] BERHASIL POSTING: {pesan}")
        else:
            print(f"[{datetime.datetime.now()}] GAGAL: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] ERROR: {str(e)}")

# --- 3. PENJADWALAN ---
# Sesuai permintaan: 7 pagi, 12 siang, 5 sore, 9 malam
schedule.every().day.at("07:00").do(kirim_cast)
schedule.every().day.at("12:00").do(kirim_cast)
schedule.every().day.at("17:00").do(kirim_cast)
schedule.every().day.at("21:19").do(kirim_cast)

print("="*50)
print("Bot Auto Yapping Farcaster (Base Focus) ACTIVE")
print("Target: 07:00, 12:00, 17:00, 21:00 (with 1-15m random delay)")
print("Model: Gemini 2.0 Flash")
print("="*50)

# --- 4. RUN LOOP ---
while True:
    schedule.run_pending()
    time.sleep(30)