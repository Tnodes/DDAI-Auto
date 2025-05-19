import time
import random
from src.client.ddai_client import DDAIClient
from src.utils.retry import retry_with_backoff
from src.utils.logger import logger

class ExtensionPingTask:
    def __init__(self):
        self.client = DDAIClient()
        self.running = True

    def stop(self):
        self.running = False

    def run(self, accounts):
        while self.running:
            for acc in accounts:
                if not self.running:
                    break
                    
                logger.info(f"[EXTENSION] UserId: {acc['userId']}")
                try:
                    def onchain_request():
                        return self.client.onchain_trigger(acc['accessToken'])
                    
                    onchain = retry_with_backoff(onchain_request)
                    if onchain.get('error', {}).get('code') == 401:
                        logger.error(f"[EXTENSION] UserId: {acc['userId']} - Invalid or expired token (onchain_trigger)")
                        continue
                    
                    requests_total = onchain.get("data", {}).get("requestsTotal", 0)
                    logger.info(f"[EXTENSION] UserId: {acc['userId']} - Onchain Trigger Success - Total Requests: {requests_total}")
                    
                    delay = random.uniform(2, 5)
                    logger.info(f"Waiting {delay:.2f} seconds before model response...")
                    time.sleep(delay)
                    
                    def model_request():
                        return self.client.model_response(acc['accessToken'])
                    
                    model = retry_with_backoff(model_request)
                    if model.get('error', {}).get('code') == 401:
                        logger.error(f"[EXTENSION] UserId: {acc['userId']} - Invalid or expired token (model_response)")
                        continue
                    
                    throughput = model.get("data", {}).get("throughput", 0)
                    formatted_throughput = f"{throughput}%"
                    logger.info(f"[EXTENSION] UserId: {acc['userId']} - Throughput: {formatted_throughput}")
                    
                except Exception as e:
                    logger.error(f"Extension actions failed for {acc['userId']}: {e}")
                    error_delay = random.uniform(15, 30)
                    logger.info(f"Error occurred. Waiting {error_delay:.2f} seconds before next account...")
                    time.sleep(error_delay)
            
            if self.running:
                logger.info("Waiting 60 seconds before next ping cycle...")
                for i in range(60):
                    if not self.running:
                        break
                    if i % 10 == 0:  # Log every 10 seconds
                        logger.info(f"Next ping cycle in {60-i} seconds...")
                    time.sleep(1) 