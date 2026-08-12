import sqlite3

db = sqlite3.connect("cryptolabx.db")
data = db.cursor()

# create member table
data.execute("""
CREATE TABLE IF NOT EXISTS members (
    mem_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    email VARCHAR(100)
)
""")

# create book table
data.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100),
    author VARCHAR(100),
    available INTEGER DEFAULT 1
)
""")

# create transaction table
data.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    mem_id INTEGER,
    issue_date TEXT,
    return_date TEXT,
    fine REAL DEFAULT 0
)
""")

db.commit()
db.close()

print("Database setup completed")