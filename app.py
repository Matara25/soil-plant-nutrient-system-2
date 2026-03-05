from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Single shared in-memory connection
conn = sqlite3.connect(':memory:', check_same_thread=False)
conn.row_factory = sqlite3.Row

def init_db():
    print("Creating database tables...")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS farms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            farm_name TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    print("Database tables created successfully!")

@app.route('/')
def home():
    return jsonify({
        'message': 'SoilDoctor API Server',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'users': '/api/users',
            'farms': '/api/farms',
            'user_farms': '/api/users/<user_id>/farms'
        }
    })

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    cursor = conn.execute(
        'INSERT INTO users (username, email, full_name) VALUES (?, ?, ?)',
        (data['username'], data['email'], data['full_name'])
    )
    conn.commit()
    user_id = cursor.lastrowid
    return jsonify({'id': user_id, 'message': 'User created'}), 201

@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = conn.execute('SELECT * FROM users').fetchall()
    return jsonify([dict(user) for user in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(user))

@app.route('/api/farms', methods=['POST', 'PUT'])
def create_farm():
    data = request.get_json()
    if request.method == 'POST':
        cursor = conn.execute(
            'INSERT INTO farms (user_id, farm_name, latitude, longitude) VALUES (?, ?, ?, ?)',
            (data['user_id'], data['farm_name'], data.get('latitude'), data.get('longitude'))
        )
        message = 'Farm created'
        farm_id = cursor.lastrowid
    elif request.method == 'PUT':
        conn.execute(
            'UPDATE farms SET farm_name = ?, latitude = ?, longitude = ? WHERE id = ?',
            (data['farm_name'], data.get('latitude'), data.get('longitude'), data['id'])
        )
        message = 'Farm updated'
        farm_id = data['id']
    conn.commit()
    return jsonify({'id': farm_id, 'message': message}), 201

@app.route('/api/users/<int:user_id>/farms', methods=['GET'])
def get_user_farms(user_id):
    farms = conn.execute(
        'SELECT * FROM farms WHERE user_id = ?', (user_id,)
    ).fetchall()
    return jsonify([dict(farm) for farm in farms])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)