import os
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
def init_IPs_table():
    DB_FILE = "bdd/openinnovation.db"
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()
    c.execute("CREATE TABLE wg_ip_pool (ip INET PRIMARY KEY, assigned_to UUID NULL, released_at TIMESTAMP NULL);")
    conn.commit()
    conn.close()