import sqlite3
from sqlite3 import Error

DB_FILE = "quiz_app.db"

def init_database():
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Error as e:
        print(f"Error creating database: {e}")
    return None

def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                correct_answers INTEGER NOT NULL,
                wrong_answers INTEGER NOT NULL,
                score REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except Error as e:
        print(f"Error creating tables: {e}")

def save_result(user_name, correct_answers, wrong_answers, score):
    conn = init_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO quiz_results (user_name, correct_answers, wrong_answers, score)
                VALUES (?, ?, ?, ?)
            """
            values = (user_name, correct_answers, wrong_answers, score)
            cursor.execute(query, values)
            conn.commit()
        except Error as e:
            print(f"Error saving result: {e}")
        finally:
            conn.close()

def get_results():
    conn = init_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM quiz_results ORDER BY timestamp DESC LIMIT 10")
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
        except Error as e:
            print(f"Error fetching results: {e}")
            return []
        finally:
            conn.close()
    return []