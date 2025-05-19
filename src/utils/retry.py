import time
from requests.exceptions import ConnectTimeout, ConnectionError, RequestException
from urllib3.exceptions import MaxRetryError
from src.utils.logger import logger

def retry_with_backoff(func, max_retries=3, initial_delay=5):
    """Retry a function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except (ConnectTimeout, ConnectionError, MaxRetryError, RequestException) as e:
            if attempt == max_retries - 1: 
                raise
            delay = initial_delay * (2 ** attempt)
            logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
            logger.info(f"Retrying in {delay} seconds...")
            time.sleep(delay) 