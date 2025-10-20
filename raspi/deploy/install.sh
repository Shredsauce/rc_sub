#!/usr/bin/env bash
set -euo pipefail
sudo apt-get update
sudo apt-get install -y python3-venv pigpio git
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -r raspi/requirements.txt
echo "Done. Use: make run  (or make service)"
