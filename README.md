# Siri Computers & Mobiles - Service Tracker (Flask)

Ready-to-deploy Flask app for a small computer & mobile service shop.
Features:
- Register customer complaints (customer name, contact, item, accessories, complaint, estimation, in-date)
- Unique public status link for each complaint (e.g. /status/abc123)
- Admin panel to view and update complaints (simple username/password)
- Modern dark theme UI
- Uses SQLite by default; can be pointed to PostgreSQL with DATABASE_URL env

## Quick start (local)
1. Create a virtualenv and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
2. Install:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and change values (IMPORTANT: change ADMIN_PASS and SECRET_KEY).
4. Run:
   ```bash
   python app.py
   ```
5. Open http://127.0.0.1:5000

## Deploy on Render
1. Create a GitHub repo and push this project.
2. On Render, create a new **Web Service** and connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Set environment variables (on Render dashboard):
   - `ADMIN_USER` (optional)
   - `ADMIN_PASS` (REQUIRED - change it)
   - `SECRET_KEY` (REQUIRED)
   - `DATABASE_URL` (optional, for Postgres)

## Notes on security
- This project uses a simple admin auth for convenience. For production, secure admin with a stronger auth system (OAuth, hashed passwords, or at least store hashed pass).
- Use HTTPS in production (Render provides it).
- Change `ADMIN_PASS` and `SECRET_KEY` before deploying.

