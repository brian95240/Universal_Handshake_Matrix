
import sys
import os
import json
import importlib
import logging
from typing import Dict, List

class SystemVerifier:
    def __init__(self):
        self.logger = logging.getLogger('SystemVerifier')
        self.required_components = {
            'foundation': ['aggregator_connector.py', 'api_key_manager.py'],
            'discovery': ['dorking_module.js', 'validation_pipeline.py', 'trigger_system.py'],
            'funnel_replication': ['competitor_analysis.py', 'template_generator.vue', 'ab_testing.js'],
            'autonomous_operation': ['performance_analyzer.py', 'budget_allocator.py', 'campaign_generator.py']
        }

    def verify_file_structure(self) -> bool:
        """Verify all required files exist"""
        missing_files = []

        for directory, files in self.required_components.items():
            if not os.path.exists(directory):
                missing_files.append(f"Directory '{directory}' not found")
                continue

            for file in files:
                if not os.path.exists(os.path.join(directory, file)):
                    missing_files.append(f"File '{directory}/{file}' not found")

        if missing_files:
            self.logger.error("Missing files detected:\n" + "\n".join(missing_files))
            return False
        return True

    def verify_config(self) -> bool:
        """Verify configuration files"""
        try:
            with open('config/deployment.json', 'r') as f:
                config = json.load(f)

            required_keys = ['environment', 'database', 'vault', 'logging', 'system']
            missing_keys = [key for key in required_keys if key not in config]

            if missing_keys:
                self.logger.error(f"Missing configuration keys: {missing_keys}")
                return False
            return True
        except Exception as e:
            self.logger.error(f"Configuration verification failed: {str(e)}")
            return False

    def verify_dependencies(self) -> bool:
        """Verify Python dependencies"""
        try:
            with open('requirements.txt', 'r') as f:
                requirements = f.read().splitlines()

            missing_deps = []
            for req in requirements:
                try:
                    if req:
                        module_name = req.split('==')[0]
                        importlib.import_module(module_name)
                except ImportError:
                    missing_deps.append(req)

            if missing_deps:
                self.logger.error(f"Missing dependencies: {missing_deps}")
                return False
            return True
        except Exception as e:
            self.logger.error(f"Dependency verification failed: {str(e)}")
            return False

    def verify_permissions(self) -> bool:
        """Verify file permissions"""
        try:
            files_to_check = ['start.sh', 'deploy.py', 'main.py']
            for file in files_to_check:
                if not os.access(file, os.R_OK | os.X_OK):
                    self.logger.error(f"Insufficient permissions for {file}")
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Permission verification failed: {str(e)}")
            return False

    def run_verification(self) -> Dict[str, bool]:
        """Run all verification checks"""
        results = {
            'file_structure': self.verify_file_structure(),
            'configuration': self.verify_config(),
            'dependencies': self.verify_dependencies(),
            'permissions': self.verify_permissions()
        }

        return results

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    verifier = SystemVerifier()
    results = verifier.run_verification()

    # Print results
    print("\nSystem Verification Results:")
    for check, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{check.replace('_', ' ').title()}: {status}")

    # Overall status
    if all(results.values()):
        print("\nAll checks passed! System is ready to start.")
        return 0
    else:
        print("\nSome checks failed. Please fix the issues before starting the system.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
