#!/bin/bash

# Create the python environment
python3 -m venv .venv
source .venv/bin/activate

# Install the requirements
echo "Installing requirements..."
pip install -r "requirements.txt"
echo "Requirements installed successfully."

# Change directory to within the AssociationMatrix folder
cd AssociationMatrix
parent_dir=$(dirname "$(pwd)")
models_dir="./models"
out_dir="./out"

# Check if the models directory exists
if [ -d "$models_dir" ]; then
    echo "Models directory already exists. Skipping download from Hugging Face."
else
    # Create models directory
    mkdir -p "$models_dir"
    
    # Download file from Hugging Face (replace with the actual URL)
    hugging_face_url="https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q5_K_M.gguf"
    wget "$hugging_face_url" -O "$models_dir/13B-chat-GGUF-q5_K_M.gguf"
    echo "File downloaded from Hugging Face successfully."
fi

if [ -d "$out_dir" ]; then
    echo "Output directory already exists. Skipping creation."
else
    # Create output directory
    mkdir -p "$out_dir"
    echo "Output directory created successfully."
fi