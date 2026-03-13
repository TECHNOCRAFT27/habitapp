# Habit Tracker — Flask App

A beautiful mobile-first habit tracker with user accounts, SQLite database,
and a responsive UI that works on phone, tablet, and desktop.

## Setup (Arch Linux)

### 1. Install Python & pip (if not already)
```bash
sudo pacman -S python python-pip
```

### 2. Create a virtual environment (recommended)
```bash
cd habitapp
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install flask werkzeug
```

### 4. Run the app
```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

---

## Access from phone / tablet on same Wi-Fi

1. Find your laptop's local IP:
   ```bash
   ip addr show | grep 'inet ' | grep -v 127
   # e.g. 192.168.1.42
   ```

2. On your phone browser, go to: `http://192.168.1.42:5000`

The app works fully from mobile — add it to your home screen for an app-like experience!

---

## Production tips

- Change `app.secret_key` in `app.py` to a fixed secret string
- Use `gunicorn` for production serving:
  ```bash
  pip install gunicorn
  gunicorn -w 4 -b 0.0.0.0:5000 app:app
  ```

## Files
```
habitapp/
├── app.py              # Flask backend + all API routes
├── habits.db           # SQLite database (auto-created on first run)
├── requirements.txt
└── templates/
    ├── login.html      # Login / register page
    └── app.html        # Main app (today, tracker, progress, habits, notes)
```
