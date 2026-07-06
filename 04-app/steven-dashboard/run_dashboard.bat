@echo off
cd /d "%~dp0"
streamlit run steven_dashboard.py --server.headless true
