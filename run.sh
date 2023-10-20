#!/bin/bash

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip is not installed. Please install pip."
    exit 1
fi

# Check if Python 3 is installed and attempt to install it if not
if ! command -v python3 &> /dev/null
then
    echo "python3 is not installed. Please install python3."
    exit 1
fi

# Install Python dependencies
pip install -r requirements.txt

# Run the program
python3 program.py
