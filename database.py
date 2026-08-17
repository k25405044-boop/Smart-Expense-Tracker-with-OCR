import sqlite3

DB_NAME = "expenses.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop TEXT,
            amount REAL,
            date TEXT,
            category TEXT,
            ocr_text TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_expense(shop, amount, date, category, ocr_text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (shop, amount, date, category, ocr_text)
        VALUES (?, ?, ?, ?, ?)
    """, (shop, amount, date, category, ocr_text))

    conn.commit()
    conn.close()


def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM expenses
        ORDER BY id DESC
    """)

    expenses = cursor.fetchall()

    conn.close()

    return expenses


def get_total():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")

    result = cursor.fetchone()[0]

    conn.close()

    return result if result else 0