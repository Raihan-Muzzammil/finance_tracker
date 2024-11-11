import sqlite3
from models import User

def create_db():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT
                    )''')
    conn.commit()
    conn.close()

def register_user(username, password):
    user = User(username, password)
    user.save_to_db()