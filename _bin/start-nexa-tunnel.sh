#!/usr/bin/env bash
set -euo pipefail
TUNNEL="sobrr-tunnel"
LOCAL_URL="${1:-http://localhost:8501}"
HOSTNAME="${2:-nexa.mooreawareness.com}"
cd "$(dirname "$0")"
./cloudflared.exe tunnel --config ~/.cloudflared/config.yml run "$TUNNEL"
