# RCSub Repo

- GitHub Pages site lives in **/docs**
- Raspberry Pi code and deploy scripts live in **/raspi**

## Quick Start on the Pi
```bash
ssh pi@<pi-host>
git clone git@github.com:<you>/<repo>.git rcsub
cd rcsub
make setup   # installs pigpio, creates venv, installs requirements
make run     # run foreground
make service # install as systemd service
```

## Update flow
- Commit/push from your dev machine.
- On the Pi:
  ```bash
  cd ~/rcsub
  make update
  ```
- (Optional) Use the provided GitHub Action to auto-SSH and pull+restart on each push. Add repository secrets: `PI_HOST`, `PI_USER`, `PI_KEY` (private key), `PI_PATH` (e.g., `/home/pi/rcsub`).

## GitHub Pages from /docs
- Settings → Pages → Build from branch → `main` / `/docs`
- If your repo is `rcsub`, keep `baseurl: /rcsub` in `docs/_config.yml`.
