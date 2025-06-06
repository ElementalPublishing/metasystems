"""
pypiextractor.py

A utility to extract a package name from a PyPI URL, generate the pip install command,
and store it in an SQLite database for later use.

Usage (CLI):
    python pypiextractor.py
    # Enter a PyPI URL when prompted

Usage (as a library):
    from pypiextractor.pypiextractor import save_pip_command_from_url
    save_pip_command_from_url("https://pypi.org/project/requests/")
"""

import sqlite3
import re
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "pypi_installs.db")

def extract_package_name(pypi_url):
    """Extract the package name from a PyPI URL."""
    match = re.search(r"pypi\.org/project/([^/]+)/?", pypi_url)
    if match:
        return match.group(1)
    raise ValueError("Invalid PyPI URL")

def save_install_command(package_name):
    """Save the pip install command for a package to the database."""
    command = f"pip install {package_name}"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS install_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_name TEXT NOT NULL,
            command TEXT NOT NULL
        )
    """)
    cur.execute("INSERT INTO install_commands (package_name, command) VALUES (?, ?)", (package_name, command))
    conn.commit()
    conn.close()
    print(f"Saved: {command}")

def save_pip_command_from_url(pypi_url):
    """Extract package name from URL and save the pip install command."""
    package_name = extract_package_name(pypi_url)
    save_install_command(package_name)

def main():
    url = input("Enter PyPI package URL: ").strip()
    try:
        save_pip_command_from_url(url)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()