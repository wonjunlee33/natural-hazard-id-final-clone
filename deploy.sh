#!/bin/bash

Setup the API
echo "Setting up API..."
cd "$(dirname "$0")/api"
bash setup_api.sh
cd ..

# Setup the frontend
echo "Setting up frontend..."   
cd "frontend"
bash setup_frontend.sh
cd ..

# Setup the tools for generating the association matrix and confusion matrix
echo "Setting up tools..."
cd "tools"
bash setup_tools.sh