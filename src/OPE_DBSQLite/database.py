import sqlite3

DB_NAME = "example.db"
TABLE_NAME = "my_table"  # Placeholder


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()
    cursor = conn.cursor()

    # TODO: Add schema here
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        );
    """)

    conn.commit()
    conn.close()