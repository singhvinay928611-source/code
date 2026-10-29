# JobHunter — Full-Stack Job Search & Application Tracker

A starter full-stack web application built with HTML, CSS, JavaScript, Python Flask and SQLite.

## Features

- Register and sign in
- Password hashing
- Search sample jobs by keyword, location, category and job type
- Save and unsave jobs
- Application tracker with statuses: Saved, Applied, Interview, Offer, Rejected
- Add notes to each saved application
- Summary counts for saved jobs, applications, interviews and offers
- Responsive desktop/mobile UI
- SQLite data persists between runs

## Requirements

- Python 3.10+
- A web browser
- Internet for installing packages and loading the optional Google Font
- No API key required

## Windows setup

1. Extract the ZIP and open the folder in VS Code.
2. Open Terminal > New Terminal.
3. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

4. Activate it:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   If using Command Prompt, run `.venv\Scripts\activate.bat`.

5. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Optional: copy `.env.example` to `.env` and set `FLASK_SECRET_KEY` to a long random secret.
7. Start the app:

   ```powershell
   python app.py
   ```

8. Visit http://127.0.0.1:5000 and create an account.

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and set FLASK_SECRET_KEY
python app.py
```

Then open http://127.0.0.1:5000.

## Project structure

- `app.py`: Flask routes, authentication and database access
- `templates/index.html`: frontend markup
- `static/style.css`: styling and responsive layout
- `static/app.js`: frontend behavior and API calls
- `requirements.txt`: dependencies
- `.env.example`: configuration template
- `jobs.db`: created automatically at first startup

## Important demo-data note

The listings are sample/demo records. Their `example.com` apply URLs are placeholders, not live job postings. To show real vacancies, integrate a permitted job data API or an authorized feed, respect each provider's terms, and add source attribution and freshness dates.

## Production notes

This is a learning/demo starter. Before public deployment, use HTTPS, a strong secret, CSRF protection, login rate limiting, secure cookie settings, a production WSGI server, backups, monitoring and appropriate privacy practices. Avoid scraping job boards unless their terms and permissions allow it.
