import os
from dotenv import load_dotenv

load_dotenv()

REF_CODE = ""
REGISTER_URL = "https://auth.ddai.network/register"
LOGIN_URL = "https://auth.ddai.network/login"
CLOUDFLARE_SITEKEY = "0x4AAAAAABdw7Ezbqw4v6Kr1"

# Get the project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
RESULTS_DIR = os.path.join(ROOT_DIR, 'results')

# Create directories if they don't exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

CAPTCHA_API_KEY = os.getenv('CAPTCHA_API_KEY') 