from flask import Flask, request, jsonify, session, render_template, redirect, url_for
import sqlite3, hashlib, os, json
from datetime import datetime, date
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(32)  # Change to a fixed string in production
DB = os.path.join(os.path.dirname(__file__), 'habits.db')

# ─── DB SETUP ────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            color TEXT DEFAULT '#b8836a',
            icon TEXT DEFAULT '✨',
            created_at TEXT DEFAULT (datetime('now')),
            archived INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            check_date TEXT NOT NULL,
            UNIQUE(habit_id, check_date),
            FOREIGN KEY (habit_id) REFERENCES habits(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            month TEXT NOT NULL,
            content TEXT DEFAULT '',
            UNIQUE(user_id, month),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ─── AUTH DECORATOR ──────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        return f(*args, **kwargs)
    return decorated

# ─── PAGE ROUTES ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('app.html', username=session.get('username'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ─── AUTH API ────────────────────────────────────────────────────────────────

@app.route('/api/register', methods=['POST'])
def register():
    d = request.json
    username = (d.get('username') or '').strip()
    email = (d.get('email') or '').strip().lower()
    pw = d.get('password') or ''
    if not username or not email or not pw:
        return jsonify({'error': 'All fields required'}), 400
    if len(pw) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    try:
        with get_db() as db:
            db.execute('INSERT INTO users (username, email, password_hash) VALUES (?,?,?)',
                       (username, email, hash_pw(pw)))
        return jsonify({'ok': True})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username or email already exists'}), 409

@app.route('/api/login', methods=['POST'])
def login():
    d = request.json
    identifier = (d.get('identifier') or '').strip()
    pw = d.get('password') or ''
    with get_db() as db:
        user = db.execute(
            'SELECT * FROM users WHERE username=? OR email=?', (identifier, identifier)
        ).fetchone()
    if not user or user['password_hash'] != hash_pw(pw):
        return jsonify({'error': 'Invalid credentials'}), 401
    session['user_id'] = user['id']
    session['username'] = user['username']
    return jsonify({'ok': True, 'username': user['username']})

@app.route('/api/me')
@login_required
def me():
    with get_db() as db:
        user = db.execute('SELECT id, username, email, created_at FROM users WHERE id=?',
                          (session['user_id'],)).fetchone()
    return jsonify(dict(user))

# ─── HABITS API ──────────────────────────────────────────────────────────────

@app.route('/api/habits', methods=['GET'])
@login_required
def get_habits():
    with get_db() as db:
        habits = db.execute(
            'SELECT * FROM habits WHERE user_id=? AND archived=0 ORDER BY id',
            (session['user_id'],)
        ).fetchall()
    return jsonify([dict(h) for h in habits])

@app.route('/api/habits', methods=['POST'])
@login_required
def add_habit():
    d = request.json
    name = (d.get('name') or '').strip()
    if not name:
        return jsonify({'error': 'Name required'}), 400
    with get_db() as db:
        cur = db.execute(
            'INSERT INTO habits (user_id, name, color, icon) VALUES (?,?,?,?)',
            (session['user_id'], name, d.get('color','#b8836a'), d.get('icon','✨'))
        )
        habit_id = cur.lastrowid
        habit = db.execute('SELECT * FROM habits WHERE id=?', (habit_id,)).fetchone()
    return jsonify(dict(habit))

@app.route('/api/habits/<int:hid>', methods=['PUT'])
@login_required
def update_habit(hid):
    d = request.json
    with get_db() as db:
        db.execute(
            'UPDATE habits SET name=?, color=?, icon=? WHERE id=? AND user_id=?',
            (d.get('name'), d.get('color','#b8836a'), d.get('icon','✨'), hid, session['user_id'])
        )
    return jsonify({'ok': True})

@app.route('/api/habits/<int:hid>', methods=['DELETE'])
@login_required
def delete_habit(hid):
    with get_db() as db:
        db.execute('DELETE FROM checkins WHERE habit_id=? AND user_id=?', (hid, session['user_id']))
        db.execute('DELETE FROM habits WHERE id=? AND user_id=?', (hid, session['user_id']))
    return jsonify({'ok': True})

# ─── CHECKINS API ────────────────────────────────────────────────────────────

@app.route('/api/checkins', methods=['GET'])
@login_required
def get_checkins():
    month = request.args.get('month', date.today().strftime('%Y-%m'))
    with get_db() as db:
        rows = db.execute(
            "SELECT habit_id, check_date FROM checkins WHERE user_id=? AND check_date LIKE ?",
            (session['user_id'], month + '%')
        ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/checkins/toggle', methods=['POST'])
@login_required
def toggle_checkin():
    d = request.json
    habit_id = d.get('habit_id')
    check_date = d.get('date')  # YYYY-MM-DD
    with get_db() as db:
        existing = db.execute(
            'SELECT id FROM checkins WHERE habit_id=? AND check_date=? AND user_id=?',
            (habit_id, check_date, session['user_id'])
        ).fetchone()
        if existing:
            db.execute('DELETE FROM checkins WHERE id=?', (existing['id'],))
            return jsonify({'checked': False})
        else:
            db.execute(
                'INSERT INTO checkins (habit_id, user_id, check_date) VALUES (?,?,?)',
                (habit_id, session['user_id'], check_date)
            )
            return jsonify({'checked': True})

@app.route('/api/stats', methods=['GET'])
@login_required
def get_stats():
    month = request.args.get('month', date.today().strftime('%Y-%m'))
    uid = session['user_id']
    with get_db() as db:
        habits = db.execute(
            'SELECT * FROM habits WHERE user_id=? AND archived=0', (uid,)
        ).fetchall()
        checkins = db.execute(
            "SELECT habit_id, check_date FROM checkins WHERE user_id=? AND check_date LIKE ?",
            (uid, month + '%')
        ).fetchall()
    
    # Days in month
    y, m = map(int, month.split('-'))
    import calendar
    num_days = calendar.monthrange(y, m)[1]
    today = date.today()
    
    checked_set = {(r['habit_id'], r['check_date']) for r in checkins}
    habit_list = [dict(h) for h in habits]
    
    # Per-habit stats
    for h in habit_list:
        done = sum(1 for d in range(1, num_days+1)
                   if (h['id'], f"{month}-{d:02d}") in checked_set)
        h['done'] = done
        h['total'] = num_days
        h['pct'] = round(done / num_days * 100) if num_days else 0
    
    # Daily totals
    daily = []
    for d in range(1, num_days+1):
        day_str = f"{month}-{d:02d}"
        done = sum(1 for h in habit_list if (h['id'], day_str) in checked_set)
        pct = round(done / len(habit_list) * 100) if habit_list else 0
        daily.append({'day': d, 'done': done, 'pct': pct})
    
    # Streak (consecutive perfect days up to today)
    streak = 0
    for d in range(num_days, 0, -1):
        day_str = f"{month}-{d:02d}"
        if datetime.strptime(day_str, '%Y-%m-%d').date() > today:
            continue
        perfect = habit_list and all((h['id'], day_str) in checked_set for h in habit_list)
        if perfect:
            streak += 1
        else:
            break
    
    total_checked = len(checkins)
    possible = len(habit_list) * num_days
    rate = round(total_checked / possible * 100) if possible else 0
    
    return jsonify({
        'habits': habit_list,
        'daily': daily,
        'streak': streak,
        'total_checked': total_checked,
        'rate': rate,
        'num_habits': len(habit_list)
    })

# ─── NOTES API ───────────────────────────────────────────────────────────────

@app.route('/api/notes', methods=['GET'])
@login_required
def get_notes():
    month = request.args.get('month', date.today().strftime('%Y-%m'))
    with get_db() as db:
        row = db.execute(
            'SELECT content FROM notes WHERE user_id=? AND month=?',
            (session['user_id'], month)
        ).fetchone()
    return jsonify({'content': row['content'] if row else ''})

@app.route('/api/notes', methods=['POST'])
@login_required
def save_notes():
    d = request.json
    month = d.get('month', date.today().strftime('%Y-%m'))
    with get_db() as db:
        db.execute(
            'INSERT INTO notes (user_id, month, content) VALUES (?,?,?) '
            'ON CONFLICT(user_id, month) DO UPDATE SET content=excluded.content',
            (session['user_id'], month, d.get('content', ''))
        )
    return jsonify({'ok': True})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
