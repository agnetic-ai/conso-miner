import json
import urllib.request
import urllib.error

SUPABASE_URL = "https://jzxlayjrsdbyzykuiqns.supabase.co"
ANON_KEY = "sb_publishable_clAiRg6ffCznEAtg_bn19Q_yY0W5Hyd"

class DailyClaimer:
    @staticmethod
    def claim_daily(access_token, proxy=None):
        url = f"{SUPABASE_URL}/rest/v1/rpc/claim_daily_mission"
        headers = {
            "apikey": ANON_KEY,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "p_mission_id": "daily_checkin",
            "p_claim_ref": None
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
                return True, res_text
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            return False, f"HTTP {e.code}: {err_body}"
        except Exception as e:
            return False, str(e)
