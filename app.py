from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'chess_club.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            birthday TEXT,
            profile_picture TEXT,
            games_played INTEGER DEFAULT 0,
            rank_position INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            white_id INTEGER NOT NULL,
            black_id INTEGER NOT NULL,
            result TEXT NOT NULL,
            played_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

init_db()

def update_ranks_after_match(white_id, black_id, result):
    conn = get_db()
    
    white = conn.execute("SELECT rank_position FROM members WHERE id=?", (white_id,)).fetchone()
    black = conn.execute("SELECT rank_position FROM members WHERE id=?", (black_id,)).fetchone()
    
    if not white or not black:
        conn.close()
        return
    
    w_rank = white['rank_position']
    b_rank = black['rank_position']
    
    if w_rank < b_rank:
        higher_rank, lower_rank = w_rank, b_rank
        higher_id, lower_id = white_id, black_id
    else:
        higher_rank, lower_rank = b_rank, w_rank
        higher_id, lower_id = black_id, white_id

    if result == 'draw':
        if lower_rank - higher_rank > 1:
            new_lower = lower_rank - 1
            conn.execute("UPDATE members SET rank_position = rank_position + 1 WHERE rank_position >= ? AND rank_position < ?", 
                        (new_lower, lower_rank))
            conn.execute("UPDATE members SET rank_position = ? WHERE id = ?", (new_lower, lower_id))

    elif (result == 'white' and white_id == lower_id) or (result == 'black' and black_id == lower_id):
        diff = abs(higher_rank - lower_rank)
        positions_up = max(1, diff // 2)
        new_lower = max(1, lower_rank - positions_up)
        new_higher = higher_rank + 1

        conn.execute("UPDATE members SET rank_position = rank_position + 1 WHERE rank_position >= ? AND rank_position < ?", 
                    (new_lower, lower_rank))
        conn.execute("UPDATE members SET rank_position = ? WHERE id = ?", (new_lower, lower_id))
        conn.execute("UPDATE members SET rank_position = ? WHERE id = ?", (new_higher, higher_id))

    conn.execute("UPDATE members SET games_played = games_played + 1 WHERE id IN (?,?)", (white_id, black_id))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/members', methods=['GET'])
def get_members():
    conn = get_db()
    members = conn.execute('SELECT * FROM members ORDER BY rank_position ASC').fetchall()
    conn.close()
    return jsonify([dict(m) for m in members])

@app.route('/api/members', methods=['POST'])
def create_member():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    password = request.form.get('password')
    birthday = request.form.get('birthday')

    if not all([full_name, email, password]):
        return jsonify({"message": "Missing fields"}),