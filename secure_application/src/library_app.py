import sqlite3
from datetime import date

# database setup
db = sqlite3.connect("library.db")
c = db.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS members (
    mem_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    available INTEGER DEFAULT 1
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    mem_id INTEGER,
    issue_date TEXT,
    return_date TEXT,
    fine INTEGER DEFAULT 0
)
""")

# adding some books if empty
c.execute("SELECT COUNT(*) FROM books")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO books (title, author) VALUES ('The Great Gatsby', 'F. Scott Fitzgerald')")
    c.execute("INSERT INTO books (title, author) VALUES ('To Kill a Mockingbird', 'Harper Lee')")
    c.execute("INSERT INTO books (title, author) VALUES ('1984', 'George Orwell')")
    c.execute("INSERT INTO books (title, author) VALUES ('Pride and Prejudice', 'Jane Austen')")
    c.execute("INSERT INTO books (title, author) VALUES ('The Catcher in the Rye', 'J.D. Salinger')")

db.commit()
db.close()


# register member
def register_member():
    name = input("Enter member name: ")
    email = input("Enter member email: ")

    db = sqlite3.connect("library.db")
    c = db.cursor()
    c.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
    db.commit()
    db.close()
    print("Member registered!")


# add book
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author: ")

    db = sqlite3.connect("library.db")
    c = db.cursor()
    c.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    db.commit()
    db.close()
    print("Book added!")


# show all members
def show_members():
    db = sqlite3.connect("library.db")
    c = db.cursor()
    c.execute("SELECT * FROM members")
    rows = c.fetchall()

    print("\n--- Members ---")
    if len(rows) == 0:
        print("No members found")
    else:
        for r in rows:
            print("ID:", r[0], "| Name:", r[1], "| Email:", r[2])
    db.close()


# show all books
def show_books():
    db = sqlite3.connect("library.db")
    c = db.cursor()
    c.execute("SELECT * FROM books")
    rows = c.fetchall()

    print("\n--- Books ---")
    if len(rows) == 0:
        print("No books found")
    else:
        for r in rows:
            if r[3] == 1:
                st = "Available"
            else:
                st = "Issued"
            print("ID:", r[0], "| Title:", r[1], "| Author:", r[2], "| Status:", st)
    db.close()


# search book
def search_book():
    keyword = input("Enter book name to search: ")

    db = sqlite3.connect("library.db")
    c = db.cursor()

    # searching using string concatenation
    query = "SELECT * FROM books WHERE title LIKE '%" + keyword + "%'"
    c.execute(query)

    rows = c.fetchall()

    print("\n--- Search Results ---")
    if len(rows) == 0:
        print("No books found")
    else:
        for r in rows:
            if r[3] == 1:
                st = "Available"
            else:
                st = "Issued"
            print("ID:", r[0], "| Title:", r[1], "| Author:", r[2], "| Status:", st)
    db.close()


# issue book
def issue_book():
    book_id = input("Enter book ID: ")
    mem_id = input("Enter member ID: ")

    db = sqlite3.connect("library.db")
    c = db.cursor()

    # check if book exists
    query = "SELECT * FROM books WHERE book_id = " + book_id
    try:
        c.execute(query)
    except Exception as e:
        print("Error:", e)
        db.close()
        return

    book = c.fetchone()
    if book is None:
        print("Book not found")
        db.close()
        return

    if book[3] == 0:
        print("Book already issued")
        db.close()
        return

    # check member
    query = "SELECT * FROM members WHERE mem_id = " + mem_id
    try:
        c.execute(query)
    except Exception as e:
        print("Error:", e)
        db.close()
        return

    member = c.fetchone()
    if member is None:
        print("Member not found")
        db.close()
        return

    today = str(date.today())

    c.execute("INSERT INTO transactions (book_id, mem_id, issue_date) VALUES (?, ?, ?)",
              (book_id, mem_id, today))
    c.execute("UPDATE books SET available = 0 WHERE book_id = ?", (book_id,))

    db.commit()
    db.close()
    print("Book issued on", today)


# return book
def return_book():
    book_id = input("Enter book ID to return: ")

    db = sqlite3.connect("library.db")
    c = db.cursor()

    query = "SELECT * FROM transactions WHERE book_id = " + book_id + " AND return_date IS NULL"
    try:
        c.execute(query)
    except Exception as e:
        print("Error:", e)
        db.close()
        return

    txn = c.fetchone()
    if txn is None:
        print("Book is not issued")
        db.close()
        return

    issue_date = date.fromisoformat(txn[3])
    today = date.today()
    days = (today - issue_date).days

    # fine calculation - Rs 5 per day after 14 days
    if days > 14:
        late = days - 14
        fine = late * 5
    else:
        late = 0
        fine = 0

    c.execute("UPDATE transactions SET return_date = ?, fine = ? WHERE transaction_id = ?",
              (str(today), fine, txn[0]))
    c.execute("UPDATE books SET available = 1 WHERE book_id = ?", (book_id,))

    db.commit()
    db.close()

    print("Book returned!")
    print("Days:", days)
    print("Late days:", late)
    print("Fine: Rs.", fine)


# calculate fine for a member
def calculate_fine():
    mem_id = input("Enter member ID: ")

    db = sqlite3.connect("library.db")
    c = db.cursor()

    query = "SELECT SUM(fine) FROM transactions WHERE mem_id = " + mem_id
    try:
        c.execute(query)
    except Exception as e:
        print("Error:", e)
        db.close()
        return

    result = c.fetchone()
    total = result[0] if result[0] else 0
    print("Total fine for member", mem_id, ": Rs.", total)
    db.close()


# show transactions
def show_transactions():
    db = sqlite3.connect("library.db")
    c = db.cursor()

    c.execute("""
        SELECT t.transaction_id, b.title, m.name, t.issue_date, t.return_date, t.fine
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        JOIN members m ON t.mem_id = m.mem_id
    """)

    rows = c.fetchall()

    print("\n--- Transactions ---")
    if len(rows) == 0:
        print("No transactions")
    else:
        for r in rows:
            ret = r[4] if r[4] else "Not returned"
            print("TX:", r[0], "| Book:", r[1], "| Member:", r[2])
            print("   Issued:", r[3], "| Returned:", ret, "| Fine:", r[5])
            print("---")
    db.close()


# delete member
def delete_member():
    mem_id = input("Enter member ID to delete: ")

    db = sqlite3.connect("library.db")
    c = db.cursor()

    query = "DELETE FROM members WHERE mem_id = " + mem_id
    try:
        c.execute(query)
    except Exception as e:
        print("Error:", e)
        db.close()
        return

    if c.rowcount > 0:
        print("Member deleted")
    else:
        print("Member not found")

    db.commit()
    db.close()


# main menu
while True:
    print("\n==========================")
    print(" LIBRARY MANAGEMENT SYSTEM")
    print("==========================")
    print("1. Register Member")
    print("2. Add Book")
    print("3. Show Members")
    print("4. Show Books")
    print("5. Search Book")
    print("6. Issue Book")
    print("7. Return Book")
    print("8. Calculate Fine")
    print("9. Show Transactions")
    print("10. Delete Member")
    print("0. Exit")

    ch = input("Enter choice: ")

    if ch == "1":
        register_member()
    elif ch == "2":
        add_book()
    elif ch == "3":
        show_members()
    elif ch == "4":
        show_books()
    elif ch == "5":
        search_book()
    elif ch == "6":
        issue_book()
    elif ch == "7":
        return_book()
    elif ch == "8":
        calculate_fine()
    elif ch == "9":
        show_transactions()
    elif ch == "10":
        delete_member()
    elif ch == "0":
        print("Goodbye!")
        break
    else:
        print("Wrong choice")
