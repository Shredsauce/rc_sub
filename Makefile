SHELL := /bin/bash
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: setup run service enable update logs status restart

setup:
	sudo apt-get update
	sudo apt-get install -y python3-venv pigpio
	sudo systemctl enable pigpiod
	sudo systemctl start pigpiod
	python3 -m venv $(VENV)
	$(PIP) install -U pip
	$(PIP) install -r raspi/requirements.txt

run:
	$(PY) raspi/rc_dashboard.py

service: /etc/systemd/system/rcsub-dashboard.service
	sudo systemctl daemon-reload
	sudo systemctl enable rcsub-dashboard.service
	sudo systemctl start rcsub-dashboard.service

/etc/systemd/system/rcsub-dashboard.service:
	echo "[Unit]\nDescription=RC Sub Dashboard\nAfter=network-online.target pigpiod.service\nWants=network-online.target\nRequires=pigpiod.service\n\n[Service]\nUser=$$USER\nWorkingDirectory=$$(pwd)\nExecStart=$$(pwd)/.venv/bin/python $$(pwd)/raspi/rc_dashboard.py\nRestart=on-failure\n\n[Install]\nWantedBy=multi-user.target" | sudo tee /etc/systemd/system/rcsub-dashboard.service >/dev/null

update:
	git pull --rebase
	sudo systemctl restart rcsub-dashboard.service

logs:
	sudo journalctl -u rcsub-dashboard.service -f

status:
	systemctl status rcsub-dashboard.service

restart:
	sudo systemctl restart rcsub-dashboard.service
