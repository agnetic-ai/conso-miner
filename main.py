import time
import random
import datetime
from auth_manager import AuthManager
from daily_claimer import DailyClaimer
from miner import Miner

def log(name, message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] [{name}] {message}")

def run_account_cycle(auth_mgr, account):
    acc_id = account["account_id"]
    name = account.get("name", acc_id)
    proxy = account.get("proxy")

    log(name, "Refreshing auth token...")
    access_token, err = auth_mgr.refresh_session(acc_id)
    if err:
        log(name, f"❌ Auth Failed: {err}")
        return

    log(name, "🔑 Auth refreshed successfully!")

    # Check User Stats
    stats = Miner.get_user_stats(access_token, proxy)
    if stats:
        log(name, f"📊 Consoname: {stats.get('consoname')} | Total Zaps: {stats.get('total_zaps')} | Daily Zaps: {stats.get('daily_zaps_earned')} | Streak: {stats.get('current_streak')}d")

    # Claim Daily Check-in
    log(name, "Checking Daily Check-in...")
    ok_claim, msg_claim = DailyClaimer.claim_daily(access_token, proxy)
    if ok_claim:
        log(name, f"🎁 Daily Check-in Result: {msg_claim}")
    else:
        log(name, f"ℹ️ Daily Check-in Note: {msg_claim}")

    # Mine Prompt
    log(name, "Executing AI Prompt Mining...")
    ok_mine, res_mine, platform, model = Miner.mine_prompt(access_token, proxy)
    if ok_mine:
        log(name, f"⚡ Mining Success [{platform}/{model}]! Credited Zaps: {res_mine}")
    else:
        log(name, f"❌ Mining Failed [{platform}/{model}]: {res_mine}")

    # Updated Stats
    stats = Miner.get_user_stats(access_token, proxy)
    if stats:
        log(name, f"📈 New Total Zaps: {stats.get('total_zaps')} | Daily Zaps: {stats.get('daily_zaps_earned')}")

def main():
    auth_mgr = AuthManager()
    
    print("=" * 60)
    print("🚀 CONSO AI USAGE TRACKER AUTO-MINER (MULTI-ACCOUNT)")
    print("=" * 60)

    # Loop Forever
    cycle = 1
    while True:
        accounts = auth_mgr.load_accounts()
        print(f"\n--- [CYCLE #{cycle}] Processing {len(accounts)} Accounts ---")
        
        for acc in accounts:
            try:
                run_account_cycle(auth_mgr, acc)
            except Exception as e:
                log(acc.get("name", acc["account_id"]), f"⚠️ Unexpected Error: {e}")
            
            # Delay between accounts (3-8 seconds)
            time.sleep(random.randint(3, 8))

        # Sleep delay before next cycle (e.g., 3-5 minutes / 180-300 seconds)
        delay_sec = random.randint(180, 300)
        now_next = datetime.datetime.now() + datetime.timedelta(seconds=delay_sec)
        print(f"\n💤 Cycle #{cycle} completed. Sleeping {delay_sec}s until {now_next.strftime('%H:%M:%S')}...\n")
        time.sleep(delay_sec)
        cycle += 1

if __name__ == "__main__":
    main()
