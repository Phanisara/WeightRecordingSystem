#!/bin/bash

# apt-get update -y && apt-get upgrade -y

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python is not installed. Please install Python to run this script."
    exit 1
fi

cd /home/raspberrypi/planetcentric/WeightRecordingSystem_GUI

echo "raspberrypi" | sudo -S python3 main.py 