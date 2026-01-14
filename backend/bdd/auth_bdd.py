import sqlite3
from datetime import datetime, timedelta

def init_refresh_token_table():
    DB_FILE = "bdd/openinnovation.db"
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS refresh_tokens(token TEXT PRIMARY KEY, username TEXT NOT NULL, expires_at TIMESTAMP NOT NULL);")
    c.execute("CREATE TABLE IF NOT EXISTS access_tokens(token TEXT PRIMARY KEY, access_tokens TEXT NOT NULL, FOREIGN KEY(token) REFERENCES refresh_tokens(token));")
    conn.commit()
    conn.close()

def add_refresh_token_db(token: str, username: str, days_valid: int = 7):
    DB_FILE = "bdd/openinnovation.db"
    expires_at = datetime.utcnow() + timedelta(days=days_valid)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO refresh_tokens(token, username, expires_at) VALUES(?,?,?)",
              (token, username, expires_at.isoformat()))
    conn.commit()
    conn.close()
def add_access_token_db(token: str, access_token: str):
    DB_FILE = "bdd/openinnovation.db"
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO access_tokens(token, access_tokens) VALUES(?,?)",
              (token, access_token))
    conn.commit()
    conn.close()

def get_refresh_token(token: str):
    DB_FILE = "bdd/openinnovation.db"
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT expires_at FROM refresh_tokens WHERE token=?", (token,))
    row = c.fetchone()
    conn.close()
    return row
def get_access_token(token: str):
    DB_FILE = "bdd/openinnovation.db"
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT access_tokens FROM access_tokens WHERE access_tokens=?", (token,))
    row = c.fetchone()
    conn.close()
    return row

def remove_refresh_token(token: str):
    DB_FILE = "bdd/openinnovation.db"
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM refresh_tokens WHERE token=?", (token,))
    conn.commit()
    conn.close()
def remove_access_token(token: str):
    DB_FILE = "bdd/openinnovation.db"
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM access_tokens WHERE token=?", (token,))
    conn.commit()
    conn.close()