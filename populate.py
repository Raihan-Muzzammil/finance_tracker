import sqlite3

def populate_db():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Assuming user_id = 1 for now
    user_id = 1

    # Sample transactions
    transactions = [
        (user_id, 1000.0, "Salary", "2023-11-15", True),
        (user_id, 500.0, "Rent", "2023-11-10", False),
        (user_id, 200.0, "Groceries", "2023-11-12", False),
        (user_id, 150.0, "Dining Out", "2023-11-20", False),
        (user_id, 300.0, "Entertainment", "2023-11-25", False),
        (user_id, 800.0, "Bonus", "2023-12-10", True),
        (user_id, 450.0, "Bills", "2023-12-15", False),
        (user_id, 250.0, "Shopping", "2023-12-20", False)
    ]

    cursor.executemany("INSERT INTO transactions (user_id, amount, category, date, is_income) VALUES (?, ?, ?, ?, ?)", transactions)
    conn.commit()
    conn.close()

# Call this function to populate the database with sample data
populate_db()