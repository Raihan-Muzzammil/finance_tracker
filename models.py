import sqlite3

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (self.username, self.password))
        conn.commit()
        conn.close()