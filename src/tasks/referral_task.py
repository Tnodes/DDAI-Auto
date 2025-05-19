import time
import random
from src.utils import generate_email, generate_username, generate_password
from src.service.captcha_solver import solve_captcha
from src.client.ddai_client import DDAIClient
from src.utils.retry import retry_with_backoff
from src.utils.logger import logger
from src.config import CLOUDFLARE_SITEKEY, REGISTER_URL

class ReferralTask:
    def __init__(self, proxy_manager):
        self.proxy_manager = proxy_manager

    def process_referral(self, index, total):
        logger.info(f"Generating referral {index+1}/{total}")
        
        proxy = self.proxy_manager.get_random_proxy()
        email = generate_email()
        username = generate_username()
        password = generate_password()
        logger.info(f"Generated: {email}, {username}, {password}")

        if not CLOUDFLARE_SITEKEY:
            logger.error("Cloudflare sitekey is not set. Please set it in config.")
            return False

        try:
            captcha_token = solve_captcha(CLOUDFLARE_SITEKEY, REGISTER_URL)
            logger.info(f"Captcha solved: {captcha_token}")

            client = DDAIClient(proxies=proxy)
            
            def register_request():
                return client.register(email, username, password, captcha_token)
            
            reg_resp = retry_with_backoff(register_request)
            
            if reg_resp.get('status') == 'success':
                captcha_token_login = solve_captcha(CLOUDFLARE_SITEKEY, REGISTER_URL)
                
                def login_request():
                    return client.login(username, password, captcha_token_login)
                
                login_resp = retry_with_backoff(login_request)
                
                account_data = {
                    "email": email,
                    "username": username,
                    "password": password,
                    "register_response": reg_resp,
                    "login_response": login_resp
                }
                client.save_account(account_data)

                access_token = login_resp.get('data', {}).get('accessToken')
                if access_token:
                    def missions_request():
                        return client.get_missions(access_token)
                    
                    missions_resp = retry_with_backoff(missions_request)
                    missions = missions_resp.get('data', {}).get('missions', [])
                    claimed_results = []
                    for mission in missions:
                        mission_id = mission.get('_id')
                        if mission_id:
                            def claim_request():
                                return client.claim_mission(access_token, mission_id)
                            
                            claim_result = retry_with_backoff(claim_request)
                            claimed_results.append({
                                'mission_id': mission_id,
                                'title': mission.get('title'),
                                'claim_result': claim_result
                            })
                    account_data['missions'] = missions
                    account_data['claimed_results'] = claimed_results
                    client.save_account(account_data)
                else:
                    logger.error('No access token found in login response.')
            else:
                logger.error(f"Registration failed: {reg_resp}")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to process referral {index+1}: {e}")
            error_delay = random.uniform(30, 60)
            logger.info(f"Error occurred. Waiting {error_delay:.2f} seconds before next attempt...")
            time.sleep(error_delay)
            return False 