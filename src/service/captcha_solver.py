from twocaptcha import TwoCaptcha
from src.config import CAPTCHA_API_KEY

solver = TwoCaptcha(CAPTCHA_API_KEY)

def solve_captcha(site_key, url):
    result = solver.turnstile(sitekey=site_key, url=url)
    return result['code'] 