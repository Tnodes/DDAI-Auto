import requests
import json
import os
from src.config import REGISTER_URL, LOGIN_URL, REF_CODE, RESULTS_DIR
from src.utils.logger import logger

os.makedirs(RESULTS_DIR, exist_ok=True)

class DDAIClient:
    EXTENSION_HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "chrome-extension://pigpomlidebemiifjihbgicepgbamdaj",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Storage-Access": "active",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    def __init__(self, proxies=None):
        self.proxies = proxies

    def register(self, email, username, password, captcha_token):
        payload = {
            "email": email,
            "username": username,
            "password": password,
            "refCode": REF_CODE,
            "captchaToken": captcha_token
        }
        logger.info(f"Registering: {email} | {username}")
        resp = requests.post(REGISTER_URL, json=payload, proxies=self.proxies)
        logger.info(f"Register response: {resp.text}")
        return resp.json()

    def login(self, username, password, captcha_token):
        payload = {
            "username": username,
            "password": password,
            "captchaToken": captcha_token
        }
        logger.info(f"Logging in: {username}")
        resp = requests.post(LOGIN_URL, json=payload, proxies=self.proxies)
        logger.info(f"Login response: {resp.text}")
        return resp.json()

    def save_account(self, data):
        path = os.path.join(RESULTS_DIR, f"{data['username']}.json")
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved account to {path}")

    def get_missions(self, access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://auth.ddai.network/missions"
        logger.info("Fetching all missions...")
        resp = requests.get(url, headers=headers, proxies=self.proxies)
        logger.info(f"Missions response: {resp.text}")
        return resp.json()

    def claim_mission(self, access_token, mission_id):
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"https://auth.ddai.network/missions/claim/{mission_id}"
        logger.info(f"Claiming mission {mission_id}...")
        resp = requests.post(url, headers=headers, proxies=self.proxies)
        logger.info(f"Claim mission response: {resp.text}")
        return resp.json()

    def onchain_trigger(self, access_token, proxies=None):
        url = "https://auth.ddai.network/onchainTrigger"
        headers = self.EXTENSION_HEADERS.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        resp = requests.post(url, headers=headers, proxies=proxies)
        return resp.json()

    def model_response(self, access_token, proxies=None):
        url = "https://auth.ddai.network/modelResponse"
        headers = self.EXTENSION_HEADERS.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        resp = requests.get(url, headers=headers, proxies=proxies)
        return resp.json() 