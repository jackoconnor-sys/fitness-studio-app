# CA11 – Fitness Studio Booking App

A Flask web application for a fitness studio, allowing users to browse and sign up
for classes, and giving admins a dashboard to manage classes and view sign-ups.

## Features
- User registration and login (passwords hashed with Werkzeug's `generate_password_hash`)
- Browse available fitness classes and sign up for them
- View your own upcoming class sign-ups
- Separate admin registration/login flow with an admin dashboard
- Admins can add new classes and view user sign-ups
- Free trial sign-up form for prospective members
- Session management via Flask-Session
- Server-side form validation with Flask-WTF / WTForms

## Tech Stack
- Python / Flask
- SQLite
- Flask-Session, Flask-WTF, WTForms
- HTML / CSS (Jinja2 templates)

## Project Structure
```
├── app.py              # Flask routes and app logic
├── database.py         # SQLite connection helpers
├── forms.py             # WTForms form definitions
├── schema.sql            # Database schema
├── templates/            # Jinja2 HTML templates
├── static/               # CSS
└── requirements.txt
```

## Setup & Run

1. Clone the repo and create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create the database from the schema:
   ```bash
   sqlite3 app.db < schema.sql
   ```

4. Set a secret key (required for sessions):
   ```bash
   export SECRET_KEY="your-own-random-secret-key"
   ```

5. Run the app:
   ```bash
   flask run
   ```

6. Visit `http://127.0.0.1:5000` in your browser.

### Admin Access
To register or log in as an admin, you'll need the special admin code.
By default it's `bloodsweatandtears` (can be overridden by setting the
`ADMIN_SPECIAL_CODE` environment variable).

## Notes
This was built as a college assignment to practice full-stack web development with
Flask: user authentication, role-based access (regular users vs. admins), session
handling, form validation, and building out full CRUD-style flows around class
sign-ups.
