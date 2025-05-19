import os
import json
from src.utils.logger import logger

class TokenExportTask:
    def __init__(self, results_dir="results", output_file="tokens.json"):
        self.results_dir = results_dir
        self.output_file = output_file

    def extract_tokens_from_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                login_data = data.get('login_response', {}).get('data', {})
                user = login_data.get('user', {})
                user_id = str(user.get('_id'))
                access_token = login_data.get('accessToken')
                refresh_token = login_data.get('refreshToken')
                if user_id and access_token and refresh_token:
                    return {
                        'userId': user_id,
                        'accessToken': access_token,
                        'refreshtoken': refresh_token
                    }
        except Exception as e:
            logger.error(f"Failed to process {filepath}: {e}")
        return None

    def export_tokens(self):
        files = [f for f in os.listdir(self.results_dir) if f.endswith('.json')]
        accounts = []
        
        for file in files:
            filepath = os.path.join(self.results_dir, file)
            token = self.extract_tokens_from_file(filepath)
            if token:
                accounts.append(token)
                
        if not accounts:
            logger.error("No valid tokens found to export")
            return False
            
        try:
            with open(self.output_file, 'w') as f:
                json.dump(accounts, f, indent=2)
            logger.info(f"Successfully exported {len(accounts)} accounts to {self.output_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to export tokens: {e}")
            return False 