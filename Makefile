make setup      # apt + venv + pip install -r raspi/requirements.txt + enable pigpiod
make enable     # installs both services to /etc/systemd/system and enables them
make start      # starts both services now
make logs       # tails controls service logs
