import os
import random
from src.utils.logger import logger

class ProxyManager:
    def __init__(self, proxies_file="proxies.txt"):
        self.proxies_file = proxies_file
        self.proxy_list = self._load_proxies()

    def _load_proxies(self):
        if os.path.exists(self.proxies_file):
            with open(self.proxies_file) as f:
                proxies = [line.strip() for line in f if line.strip()]
            if proxies:
                logger.info(f"Proxies loaded: {len(proxies)}")
            else:
                logger.info("No proxies found, running without proxy")
            return proxies
        else:
            logger.info("Proxies file not found, running without proxy")
            return []

    def get_random_proxy(self):
        if not self.proxy_list:
            return None
        proxy_url = random.choice(self.proxy_list)
        logger.info(f"Using proxy: {proxy_url}")
        return {"http": proxy_url, "https": proxy_url} 