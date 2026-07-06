# NEXA Control — Deploy Runbook
## Local
cd NEXA/app/nexa-control
pip install -r requirements.txt
python app.py
open http://127.0.0.1:8090

## Production
- Push `phase1/personal-os-dashboard` to GitHub
- Connect repo to Render/Render/your VPS
- Set PORT if required; no other env vars required
- Database: use bundled `nexa.db` after first local run, or replace with Supabase Postgres later
