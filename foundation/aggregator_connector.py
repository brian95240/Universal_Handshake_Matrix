
import requests
from typing import Dict, List
import json
from utils.api_key_manager import APIKeyManager

class AffiliateAggregator:
    def __init__(self):
        self.key_manager = APIKeyManager()
        self.networks = {
            'shareasale': 'https://api.shareasale.com/x.cfm',
            'cj': 'https://commission-junction.com/api',
            'impact': 'https://api.impact.com'
        }

    def get_auth_headers(self, network: str) -> Dict:
        token = self.key_manager.get_token(network)
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def fetch_programs(self, network: str) -> List[Dict]:
        headers = self.get_auth_headers(network)
        response = requests.get(
            f"{self.networks[network]}/programs",
            headers=headers
        )
        return response.json()

    def fetch_offers(self, network: str, program_id: str) -> List[Dict]:
        headers = self.get_auth_headers(network)
        response = requests.get(
            f"{self.networks[network]}/offers/{program_id}",
            headers=headers
        )
        return response.json()
