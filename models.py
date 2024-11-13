import sqlite3
import bcrypt # type: ignore

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        self.password_hash = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (self.username, self.password_hash))
        conn.commit()
        conn.close()

class Transaction:
    def __init__(self, user_id, amount, category, date, is_income):
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.date = date
        self.is_income = is_income

    def save_to_db(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (user_id, amount, category, date, is_income) VALUES (?, ?, ?, ?, ?)",
                       (self.user_id, self.amount, self.category, self.date, self.is_income))
        conn.commit()
        conn.close()