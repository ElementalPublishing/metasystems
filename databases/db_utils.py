import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "metasystems.db")
SQL_DIR = os.path.join(BASE_DIR, "sql")

def run_sql_file(filename, params=None):
    """Run a SQL file from the sql directory and return the results."""
    sql_path = os.path.join(SQL_DIR, filename)
    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    results = cur.fetchall()
    conn.close()
    return results

# Example usage:
if __name__ == "__main__":
    # Count modules
    result = run_sql_file("count_modules.sql")
    print("Total modules:", result[0][0])