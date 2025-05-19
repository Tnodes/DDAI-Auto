import signal
import sys
import json
import os
from src.utils.proxy_manager import ProxyManager
from src.utils.account_manager import AccountManager
from src.tasks.extension_ping import ExtensionPingTask
from src.tasks.referral_task import ReferralTask
from src.tasks.token_export import TokenExportTask
from src.utils.logger import logger
from src.utils.banner import print_banner
from tabulate import tabulate

# Global flag for graceful shutdown
running = True

def signal_handler(signum, frame):
    global running
    logger.info("Received shutdown signal. Gracefully stopping...")
    running = False

def get_referral_code():
    config_path = "referral_code.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                if "referral_code" in config and config["referral_code"]:
                    return config["referral_code"]
        except Exception as e:
            logger.error(f"Error reading config: {e}")
    
    print("\nNo referral code found in referral_code.json")
    referral_code = input("Please enter your referral code: ").strip()
    
    try:
        config = {}
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
        
        config["referral_code"] = referral_code
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
        logger.info("Referral code saved to referral_code.json")
    except Exception as e:
        logger.error(f"Error saving config: {e}")
    
    return referral_code

def menu():
    sequence_data = [
        ["Best Mode Sequence:", "1 → 3 → 2"]
    ]
    
    options_data = [
        ["1", "Start auto reff + claim task"],
        ["2", "Start extension for all account", "Note: Make sure you have accounts in results/ directory"],
        ["3", "Export all refferal accounts", "Note: This will create/update tokens.json in root directory"]
    ]
    
    print("\n" + tabulate(sequence_data, tablefmt="grid", numalign="center", stralign="left"))
    print()
    
    print(tabulate(options_data, headers=["No", "Option", "Note"], tablefmt="grid", numalign="left", stralign="left"))
    print()
    
    choice = input("Choose [1/2/3]: ").strip()
    return choice

def main():
    # Print banner
    print_banner()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    proxy_manager = ProxyManager()
    account_manager = AccountManager()
    
    choice = menu()
    if choice == "1":
        # Get referral code before starting task
        referral_code = get_referral_code()
        if not referral_code:
            logger.error("No referral code provided. Exiting...")
            sys.exit(1)
            
        try:
            num_referrals = int(input("\nHow many referrals to generate? "))
        except Exception:
            logger.error("Invalid input. Please enter a number.")
            sys.exit(1)

        referral_task = ReferralTask(proxy_manager)
        for i in range(num_referrals):
            if not running:
                break
            referral_task.process_referral(i, num_referrals)
                
    elif choice == "2":
        accounts = account_manager.load_accounts()
        if not accounts:
            logger.error("No valid accounts found in results/ directory")
            sys.exit(1)
            
        logger.info(f"Loaded {len(accounts)} accounts from results/")
        logger.info("Starting auto-ping for all accounts (Press Ctrl+C to stop)")
        
        extension_task = ExtensionPingTask()
        try:
            extension_task.run(accounts)
        except KeyboardInterrupt:
            extension_task.stop()
            logger.info("Extension task stopped by user")
            
    elif choice == "3":
        token_export = TokenExportTask()
        if token_export.export_tokens():
            logger.info("Token export completed successfully")
        else:
            logger.error("Token export failed")
            
    else:
        print("\nInvalid choice.")

if __name__ == "__main__":
    main() 