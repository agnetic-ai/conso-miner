import json
import random
import urllib.request
import urllib.error

SUPABASE_URL = "https://jzxlayjrsdbyzykuiqns.supabase.co"
ANON_KEY = "sb_publishable_clAiRg6ffCznEAtg_bn19Q_yY0W5Hyd"

PROMPTS = [
    "Tolong jelaskan konsep dasar machine learning dan neural network.",
    "Bagaimana cara mengoptimalkan performa database MySQL untuk high traffic?",
    "Berikan contoh arsitektur microservices menggunakan Node.js dan Docker.",
    "Apa perbedaan utama antara REST API dan GraphQL?",
    "Buatkan kode Python untuk web scraping menggunakan BeautifulSoup.",
    "Jelaskan prinsip SOLID dalam pemrograman berorientasi objek.",
    "Bagaimana cara kerja insentrasi smart contract di blockchain Ethereum?"
]

MODELS = [
    {"platform": "gemini", "model": "gemini-1.5-pro", "base_zaps": 1.5, "spend": 0.02},
    {"platform": "chatgpt", "model": "gpt-4o", "base_zaps": 1.8, "spend": 0.025},
    {"platform": "claude", "model": "claude-3-5-sonnet", "base_zaps": 2.0, "spend": 0.03}
]

class Miner:
    @staticmethod
    def mine_prompt(access_token, proxy=None):
        url = f"{SUPABASE_URL}/rest/v1/rpc/append_prompt"
        headers = {
            "apikey": ANON_KEY,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        prompt = random.choice(PROMPTS)
        m_info = random.choice(MODELS)

        payload = {
            "p_entry": {
                "platform": m_info["platform"],
                "model": m_info["model"],
                "promptText": prompt,
                "promptLength": len(prompt),
                "responseLength": random.randint(300, 800)
            },
            "p_base_zaps": m_info["base_zaps"],
            "p_spend_usd": m_info["spend"]
        }

        handler = urllib.request.HTTPHandler()
        if proxy:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
        else:
            opener = urllib.request.build_opener(handler)

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        try:
            with opener.open(req) as resp:
                res_text = resp.read().decode("utf-8")
                return True, res_text, m_info["platform"], m_info["model"]
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            return False, f"HTTP {e.code}: {err_body}", m_info["platform"], m_info["model"]
        except Exception as e:
            return False, str(e), m_info["platform"], m_info["model"]

    @staticmethod
    def get_user_stats(access_token, proxy=None):
        url = f"{SUPABASE_URL}/rest/v1/consousers?select=consoname,total_zaps,daily_zaps_earned,boost_factor,current_streak"
        headers = {
            "apikey": ANON_KEY,
            "Authorization": f"Bearer {access_token}"
        }
        handler = urllib.request.HTTPHandler()
        if proxy:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
        else:
            opener = urllib.request.build_opener(handler)

        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with opener.open(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data[0] if data else None
        except Exception:
            return None
