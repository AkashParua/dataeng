import sqlite3
import os

def run_query(content: str):
    db_path = 'db/database.db'
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(content)
        conn.commit()  # Commit the transaction if it's a write operation
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if conn:
            conn.close()

run_query("SELECT * FROM table_name")