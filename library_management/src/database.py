import sqlite3


# Connect to database
db = sqlite3.connect("cryptolabx.db")
data = db.cursor()


# MEMBER REGISTRATION
data.execute("""
CREATE TABLE IF NOT EXISTS members (
    mem_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")


# BOOKS
data.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    available INTEGER NOT NULL DEFAULT 1
)
""")


# BOOK TRANSACTIONS
data.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    mem_id INTEGER NOT NULL,
    issue_date TEXT NOT NULL,
    return_date TEXT,
    fine REAL DEFAULT 0,

    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (mem_id) REFERENCES members(mem_id)
)
""")


# Save changes
db.commit()

# Close database
db.close()

print("Database and tables created successfully.")