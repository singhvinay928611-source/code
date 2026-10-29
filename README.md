# AI-Powered Smart Traffic Monitoring System — Full-stack demo

Flask + SQLite + HTML/CSS/JavaScript traffic dashboard.

## Features
- Dashboard metrics for cameras and open incidents
- Add camera locations
- Log and resolve incidents
- Simulated traffic-volume chart
- Upload traffic images for manual review
- Responsive layout and SQLite persistence

## Important limitation
This is a learning prototype, **not real AI detection**. Traffic counts are simulated, configured cameras are not live CCTV feeds, and uploaded images are stored for manual review. For a real deployment, integrate an authorized video source and a validated detection model (such as a properly licensed YOLO model), and add privacy/security controls and human verification. Do not use this demo for enforcement or safety decisions.

## Run on Ubuntu/Linux
In a terminal opened in this folder:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
cp .env.example .env
python3 app.py
```
Then open http://127.0.0.1:5000. If `.env` already exists, the copy command can be skipped.
