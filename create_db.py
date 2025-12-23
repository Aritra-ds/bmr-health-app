import sqlite3
from werkzeug.security import generate_password_hash

# Connect to SQLite database (creates database.db if it doesn't exist)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# -------------------- USERS TABLE --------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    security_q1 TEXT NOT NULL,
    security_a1 TEXT NOT NULL,
    security_q2 TEXT NOT NULL,
    security_a2 TEXT NOT NULL,
    bmr REAL
)
""")

# -------------------- BMR REPORTS TABLE (optional) --------------------
# If you want to store BMR history
cursor.execute("""
CREATE TABLE IF NOT EXISTS bmr_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL,
    bmr_value REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id)
)
""")

# -------------------- HEALTH ASSESSMENT TABLE (optional) --------------------
# If you want to store assessment history
cursor.execute("""
CREATE TABLE IF NOT EXISTS health_assessment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    smoking INTEGER,
    alcohol INTEGER,
    exercise INTEGER,
    sleep INTEGER,
    stress INTEGER,
    score INTEGER,
    risk_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id)
)
""")

# -------------------- DIET PLAN TABLE (optional) --------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS diet_plan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    bmr_value REAL,
    calories INTEGER,
    plan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id)
)
""")

# -------------------- OPTIONAL: ADD TEST USER --------------------
test_password = generate_password_hash("Test@123")
cursor.execute("""
INSERT OR IGNORE INTO user (name, email, password_hash, security_q1, security_a1, security_q2, security_a2)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    "Test User",
    "test@example.com",
    test_password,
    "Your favorite color?",
    generate_password_hash("blue"),
    "Your birth city?",
    generate_password_hash("city")
))

# Commit changes and close
conn.commit()
conn.close()

print("Database created successfully with tables and test user!")
