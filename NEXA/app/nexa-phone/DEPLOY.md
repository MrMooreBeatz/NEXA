# NEXA Phone Dashboard - Deploy Runbook

## Local run
cd NEXA/app/nexa-phone
pip install -r requirements.txt
python api.py
open http://127.0.0.1:8080

## Deploy
- Push branch `phase1/personal-os-dashboard` to GitHub.
- Connect repo to Render / VPS using `render.yaml`.
- Set required env vars:
  - `PORT=8080`
- If using another PaaS, start command:
  - `gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 60`