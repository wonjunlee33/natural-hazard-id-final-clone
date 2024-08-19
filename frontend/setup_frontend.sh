#!/bin/bash

# Create the python environment
python3 -m venv .venv
source .venv/bin/activate

# Install the requirements
echo "Installing requirements..."
pip install -r "requirements.txt"
echo "Requirements installed successfully."