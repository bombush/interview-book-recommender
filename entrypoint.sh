#!/bin/bash

python3 install/install.py

# Check if running interactively (has a TTY)
if [ -t 0 ]; then
    python3 main.py
else
    echo "Container running in non-interactive mode. Use 'docker run -it' to interact with the application."
fi