import json
import urllib.request
import urllib.error
import os

SUPABASE_URL = "https://jzxlayjrsdbyzykuiqns.supabase.co"
ANON_KEY = "sb_publishable_clAiRg6ffCznEAtg_bn19Q_yY0W5Hyd"

class AuthManager:
    def __init__(self, accounts_file=None):
        if accounts_file is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            accounts_file = os.path.join(base_dir, "accounts.json")
        self.accounts_file = accounts_file

    def load_accounts(self):
        if not os.path.exists(self.accounts_file):
            return []
        with open(self.accounts_file, "r") as f:
            return json.load(f)

    def save_accounts(self, accounts):
        with open(self.accounts_file, "w") as f:
            json.dump(accounts, f, indent=2)

    def refresh_session(self, account_id):
        accounts = self.load_accounts()
        acc = next((a for a in accounts if a["account_id"] == account_id), None)
        if not acc:
            return None, "Account not found"

        url = f"{SUPABASE_URL}/auth/v1/token?grant_type=refresh_token"
        headers = {
            "apikey": ANON_KEY,
            "Content-Type": "application/json"
        }
        payload = {"refresh_token": acc["refresh_token"]}
        data_bytes = json.dumps(payload).encode("utf-8")

        # Support Proxy if configured
        handler = urllib.request.HTTPHandler()
        if acc.get("proxy"):
            proxy_handler = urllib.request.ProxyHandler({
                "http": acc["proxy"],
                "https": acc["proxy"]
            })
            opener = urllib.request.build_opener(proxy_handler)
        else:
            opener = urllib.request.build_opener(handler)

        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
        try:
            with opener.open(req) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                new_access_token = res_data["access_token"]
                new_refresh_token = res_data["refresh_token"]

                # Update accounts.json with rotated refresh_token
                for a in accounts:
                    if a["account_id"] == account_id:
                        a["refresh_token"] = new_refresh_token
                        break
                self.save_accounts(accounts)

                return new_access_token, None
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            return None, f"HTTP Error {e.code}: {err_body}"
        except Exception as e:
            return None, str(e)
