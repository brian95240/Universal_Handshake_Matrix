
import os
import subprocess
import sys
import json
import logging
from typing import List, Dict

class Deployer:
    def __init__(self):
        self.logger = logging.getLogger('Deployer')
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """Load deployment configuration"""
        try:
            with open('config/deployment.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'environment': 'development',
                'database': {
                    'host': 'localhost',
                    'port': 5432,
                    'name': 'affiliate_matrix'
                },
                'vault': {
                    'host': 'localhost',
                    'port': 8200
                }
            }

    def check_dependencies(self) -> bool:
        """Check if all required dependencies are installed"""
        required = [
            'python-3.8',
            'postgresql',
            'nodejs',
            'vault'
        ]

        missing = []
        for dep in required:
            try:
                subprocess.run(['which', dep], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                missing.append(dep)

        if missing:
            self.logger.error(f"Missing dependencies: {', '.join(missing)}")
            return False
        return True

    def setup_database(self) -> bool:
        """Setup database schema"""
        try:
            # Execute schema file
            with open('foundation/index_schema.sql', 'r') as f:
                schema = f.read()

            subprocess.run(
                ['psql', '-d', self.config['database']['name'], '-f', '-'],
                input=schema.encode(),
                check=True
            )
            return True
        except Exception as e:
            self.logger.error(f"Database setup failed: {str(e)}")
            return False

    def setup_vault(self) -> bool:
        """Setup HashiCorp Vault"""
        try:
            # Initialize vault
            subprocess.run(['vault', 'operator', 'init'], check=True)
            return True
        except Exception as e:
            self.logger.error(f"Vault setup failed: {str(e)}")
            return False

    def install_requirements(self) -> bool:
        """Install Python requirements"""
        try:
            subprocess.run(
                ['pip', 'install', '-r', 'requirements.txt'],
                check=True
            )
            return True
        except Exception as e:
            self.logger.error(f"Requirements installation failed: {str(e)}")
            return False

    def deploy(self) -> bool:
        """Run full deployment process"""
        steps = [
            ('Checking dependencies', self.check_dependencies),
            ('Setting up database', self.setup_database),
            ('Setting up vault', self.setup_vault),
            ('Installing requirements', self.install_requirements)
        ]

        for step_name, step_func in steps:
            self.logger.info(f"Starting: {step_name}")
            if not step_func():
                self.logger.error(f"Deployment failed at: {step_name}")
                return False
            self.logger.info(f"Completed: {step_name}")

        self.logger.info("Deployment completed successfully")
        return True

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    deployer = Deployer()
    success = deployer.deploy()
    sys.exit(0 if success else 1)
