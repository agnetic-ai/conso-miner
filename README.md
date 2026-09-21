# 🚀 CONSO AI USAGE TRACKER AUTO-MINER (MULTI-ACCOUNT)

Bot automasi penambang poin **Zaps** pada ekstensi **Conso: AI Usage Tracker** berbasis **Full Pure HTTP (Python Standalone)** tanpa perlu membuka browser atau Selenium/Playwright.

---

## 📌 Fitur Utama

- ⚡ **100% Pure HTTP Request:** Menggunakan pustaka standar Python (`urllib.request` & `json`), super ringan dan bisa berjalan di VPS termurah sekalipun.
- 🔄 **Auto Token Rotation:** Otomatis memperbarui `access_token` dan `refresh_token` Supabase tanpa perlu login ulang di browser.
- 👥 **Multi-Account & Proxy Support:** Bisa menangani banyak akun sekaligus dengan opsi proxy HTTP/HTTPS terpisah per akun.
- 🎁 **Auto Daily Check-in:** Otomatis klaim *Daily Mission Check-in* setiap hari.
- 🧠 **Simulasi Multi-AI Prompt:** Mensimulasikan prompt interaksi ke ChatGPT (`gpt-4o`), Gemini (`gemini-1.5-pro`), Claude (`claude-3-5-sonnet`), dan Perplexity (`sonar-pro`) secara acak dengan delay yang natural.

---

## 📂 Struktur File Project (`/opt/conso-bot`)

```text
/opt/conso-bot/
├── accounts.json      # File konfigurasi multi-akun & session storage
├── auth_manager.py    # Logika refresh session & rotasi token Supabase
├── daily_claimer.py   # Module auto-claim daily check-in
├── miner.py           # Module simulasi prompt mining & fetch stats
├── main.py            # Script utama runner loop 24/7
└── README.md          # Panduan penggunaan
```

---

## 🔑 Cara Mengambil `refresh_token` Pertama Kali

1. Pasang ekstensi **Conso** di Chrome dan lakukan login akun Google.
2. Buka URL `chrome://extensions/` di browser Chrome, aktifkan **Developer mode** di kanan atas.
3. Pada ekstensi Conso, klik **service worker** (atau inspect background page).
4. Buka tab **Console** di DevTools, lalu jalankan perintah:
   ```javascript
   chrome.storage.local.get(null, data => console.log(JSON.stringify(data, null, 2)))
   ```
5. Cari key `sb-jzxlayjrsdbyzykuiqns-auth-token` dan ambil nilai `"refresh_token"`.

---

## ⚙️ Panduan Setup & Penggunaan

### 1. Konfigurasi `accounts.json`

Buka file `/opt/conso-bot/accounts.json` dan tambahkan daftar akun kamu:

```json
[
  {
    "account_id": "acc_1",
    "name": "Akun Utama (Beng)",
    "refresh_token": "PASTE_REFRESH_TOKEN_DISINI",
    "proxy": ""
  },
  {
    "account_id": "acc_2",
    "name": "Akun Ke-2",
    "refresh_token": "PASTE_REFRESH_TOKEN_AKUN_2",
    "proxy": "http://user:pass@ip:port"
  }
]
```

* `refresh_token`: Refresh token awal yang diambil dari Chrome. Bot akan otomatis memperbarui nilai ini di file `accounts.json` setiap kali running.
* `proxy`: *(Opsional)* Alamat proxy HTTP/HTTPS jika ingin menggunakan IP terpisah per akun. Kosongkan `""` jika tidak menggunakan proxy.

---

### 2. Jalankan Bot (Manual / Test)

```bash
python3 /opt/conso-bot/main.py
```

---

### 3. Menjalankan 24/7 di Background (Systemd Service / PM2)

#### **Menggunakan PM2:**
```bash
pm2 start /opt/conso-bot/main.py --name "conso-bot" --interpreter python3
pm2 save
```

#### **Menggunakan Systemd Daemon:**
Buat file service di `/etc/systemd/system/conso-bot.service`:
```ini
[Unit]
Description=Conso AI Usage Tracker Auto-Miner
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/conso-bot
ExecStart=/usr/bin/python3 /opt/conso-bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Aktifkan service:
```bash
systemctl daemon-reload
systemctl enable conso-bot
systemctl start conso-bot
```

Cek status & log:
```bash
systemctl status conso-bot
journalctl -u conso-bot -f
```
