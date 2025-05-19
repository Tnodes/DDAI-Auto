import os
import json
from dotenv import load_dotenv

load_dotenv()

# Get the project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
RESULTS_DIR = os.path.join(ROOT_DIR, 'results')
REFERRAL_FILE = os.path.join(ROOT_DIR, 'referral_code.json')

with open(REFERRAL_FILE, 'r') as f:
    ref_data = json.load(f)
    REF_CODE = ref_data.get("referral_code", "default_ref_code")

REGISTER_URL = "https://auth.ddai.network/register"
LOGIN_URL = "https://auth.ddai.network/login"
CLOUDFLARE_SITEKEY = "0x4AAAAAABdw7Ezbqw4v6Kr1"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

CAPTCHA_API_KEY = os.getenv('CAPTCHA_API_KEY')