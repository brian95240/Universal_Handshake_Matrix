#!/bin/bash

# Check Python version
python3 --version

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run deployment
python deploy.py

# If deployment successful, start the system
if [ $? -eq 0 ]; then
    python main.py
else
    echo "Deployment failed. Please check the logs."
    exit 1
fi
