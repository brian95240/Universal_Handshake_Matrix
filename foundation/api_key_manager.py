
import hvac
from typing import Dict
import os

class APIKeyManager:
    def __init__(self):
        self.client = hvac.Client(
            url='http://localhost:8200',
            token=os.getenv('VAULT_TOKEN')
        )
        self.mount_point = 'affiliate-keys'

    def get_token(self, network: str) -> str:
        try:
            secret = self.client.secrets.kv.v2.read_secret_version(
                path=f'{network}',
                mount_point=self.mount_point
            )
            return secret['data']['data']['token']
        except Exception as e:
            print(f"Error fetching token for {network}: {str(e)}")
            return None

    def rotate_token(self, network: str, new_token: str):
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=f'{network}',
                secret=dict(token=new_token),
                mount_point=self.mount_point
            )
        except Exception as e:
            print(f"Error rotating token for {network}: {str(e)}")
