import os
import json
import glob
from src.utils.logger import logger

class AccountManager:
    def __init__(self, results_dir="results"):
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)

    def load_accounts(self):
        account_files = glob.glob(os.path.join(self.results_dir, "*.json"))
        accounts = []
        for file in account_files:
            try:
                with open(file, "r") as f:
                    data = json.load(f)
                    login_data = data.get("login_response", {}).get("data", {})
                    user = login_data.get("user", {})
                    user_id = str(user.get("_id"))
                    access_token = login_data.get("accessToken")
                    refresh_token = login_data.get("refreshToken")
                    if user_id and access_token and refresh_token:
                        accounts.append({
                            "userId": user_id,
                            "accessToken": access_token,
                            "refreshtoken": refresh_token
                        })
            except Exception as e:
                logger.error(f"Failed to load account from {file}: {e}")
        return accounts

    def save_account(self, account_data):
        try:
            username = account_data.get("username")
            if not username:
                logger.error("Cannot save account: username is missing")
                return False

            filename = os.path.join(self.results_dir, f"{username}.json")
            with open(filename, "w") as f:
                json.dump(account_data, f, indent=4)
            logger.info(f"Account data saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to save account data: {e}")
            return False 