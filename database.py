import sqlite3
import bcrypt # type: ignore
import uuid
import datetime
from tabulate import tabulate # type: ignore
from models import User, Transaction

def create_db():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        amount REAL,
                        category TEXT,
                        date TEXT,
                        is_income BOOLEAN
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        token TEXT,
                        expiry_timestamp TIMESTAMP
                    )''')
    conn.commit()
    conn.close()


def register_user(username, password):
    user = User(username, password)
    user.save_to_db()

def authenticate_user(username, password):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        user_id, hashed_password = result
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True
    return False

def get_id(username):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0]

def create_session(user_id):
    token = str(uuid.uuid4())
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(hours=0.5)
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (user_id, token, expiry_timestamp) VALUES (?, ?, ?)", (user_id, token, expiry_time))
    conn.commit()
    conn.close()
    return token

def get_user_id_from_session(token):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM sessions WHERE token = ? AND expiry_timestamp > ?", (token, datetime.datetime.utcnow()))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def delete_session(token):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def generate_report(report_type, year, month=None):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    if report_type == 'monthly':
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-31"
        query = """
            SELECT SUM(amount) AS total_amount, category, SUM(CASE WHEN is_income THEN amount ELSE -amount END) AS net_amount
            FROM transactions
            WHERE date BETWEEN ? AND ?
            GROUP BY category
        """
    elif report_type == 'yearly':
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        query = """
            SELECT SUM(amount) AS total_amount, category, SUM(CASE WHEN is_income THEN amount ELSE -amount END) AS net_amount
            FROM transactions
            WHERE date BETWEEN ? AND ?
            GROUP BY category
        """
    elif report_type == 'categorized':
        query = """
            SELECT category, SUM(CASE WHEN is_income THEN amount ELSE -amount END) AS net_amount
            FROM transactions
            GROUP BY category
        """
    else:
        raise ValueError("Invalid report type")

    cursor.execute(query, (start_date, end_date) if report_type != 'categorized' else ())
    rows = cursor.fetchall()
    conn.close()

    headers = ["Category", "Total Amount", "Net Amount"]
    table_data = [headers] + rows

    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))


#def update_transaction(transaction_id, ...):
#    # ...

#def delete_transaction(transaction_id):
#    # ...