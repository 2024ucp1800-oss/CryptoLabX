import sqlite3
from datetime import date

# create database
db = sqlite3.connect("cryptolabx.db")
data = db.cursor()

data.execute("""
CREATE TABLE IF NOT EXISTS members (
    mem_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
)
""")

data.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    available INTEGER DEFAULT 1
)
""")

data.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    mem_id INTEGER,
    issue_date TEXT,
    return_date TEXT,
    fine INTEGER DEFAULT 0
)
""")

db.commit()
db.close()


# register a new member
def register_member():

    name = input("Enter member name: ")
    email = input("Enter member email: ")

    db = sqlite3.connect("cryptolabx.db")
    data = db.cursor()

    data.execute(
        "INSERT INTO members (name, email) VALUES (?, ?)",
        (name, email)
    )

    db.commit()
    db.close()

    print("Member added")


# add a new book
def add_book():

    title = input("Enter book title: ")
    author = input("Enter author name: ")

    db = sqlite3.connect("cryptolabx.db")
    data = db.cursor()

    data.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (title, author)
    )

    db.commit()
    db.close()

    print("Book added")


# display all members
def show_members():

    db = sqlite3.connect("cryptolabx.db")
    data = db.cursor()

    data.execute("SELECT * FROM members")

    members = data.fetchall()

    print("\n--- Members ---")

    if len(members) == 0:
        print("No members found")

    else:
        for member in members:
            print(
                "ID:", member[0],
                "Name:", member[1],
                "Email:", member[2]
            )

    db.close()


# display all books
def show_books():

    db = sqlite3.connect("cryptolabx.db")
    data = db.cursor()

    data.execute("SELECT * FROM books")

    books = data.fetchall()

    print("\n--- Books ---")

    if len(books) == 0:
        print("No books found")

    else:
        for book in books:

            if book[3] == 1:
                status = "Available"
            else:
                status = "Issued"

            print(
                "ID:", book[0],
                "Title:", book[1],
                "Author:", book[2],
                "Status:", status
            )

    db.close()


# search book
def search_book():

    word = input("Enter book name: ")

    db = sqlite3.connect("cryptolabx.db")
    data = db.cursor()

    data.execute(
        "SELECT * FROM books WHERE title LIKE ?",
        ("%" + word + "%",)
    )

    books = data.fetchall()

    print("\n--- Search Result ---")

    if len(books) == 0:

        print("Book not found")

    else:

        for book in books:

            if book[3] == 1:
                status = "Available"
            else:
                status = "Issued"

            print(
                "ID:", book[0],
                "Title:", book[1],
                "Author:", book[2],
                "Status:", status
            )

    db.close()


# issue a book
def issue_book():

    book_id = input("Enter book ID: ")
    mem_id = input("Enter member ID: ")

    db = sqlite3.connect("cryptolabx.db")
    data = db.cursor()

    # check book
    data.execute(
        "SELECT * FROM books WHERE book_id = ?",
        (book_id,)
    )

    book = data.fetchone()

    if book is None:

        print("Book does not exist")
        db.close()
        return

    # check book availability
    if book[3] == 0:

        print("Book is already issued")
        db.close()
        return

    # check member
    data.execute(
        "SELECT * FROM members WHERE mem_id = ?",
        (mem_id,)
    )

    member = data.fetchone()

    if member is None:

        print("Member does not exist")
        db.close()
        return

    today = str(date.today())

    # add transaction
    data.execute("""
        INSERT INTO transactions
        (book_id, mem_id, issue_date)
        VALUES (?, ?, ?)
    """, (book_id, mem_id, today))

    # make book unavailable
    data.execute(
        "UPDATE books SET available = 0 WHERE book_id = ?",
        (book_id,)
    )

    db.commit()
    db.close()

    print("Book issued")
    print("Date:", today)


# return a book
def return_book():

    book_id = input("Enter book ID: ")

    db = sqlite3.connect("cryptolabx.db")
    data = db.cursor()

    data.execute("""
        SELECT * FROM transactions
        WHERE book_id = ? AND return_date IS NULL
    """, (book_id,))

    transaction = data.fetchone()

    if transaction is None:

        print("Book is not issued")
        db.close()
        return

    issue_date = date.fromisoformat(transaction[3])
    today = date.today()

    days = (today - issue_date).days

    # 14 days are allowed
    if days > 14:

        late_days = days - 14
        fine = late_days * 5

    else:

        late_days = 0
        fine = 0

    # update transaction
    data.execute("""
        UPDATE transactions
        SET return_date = ?, fine = ?
        WHERE transaction_id = ?
    """, (str(today), fine, transaction[0]))

    # make book available
    data.execute(
        "UPDATE books SET available = 1 WHERE book_id = ?",
        (book_id,)
    )

    db.commit()
    db.close()

    print("Book returned")
    print("Days:", days)
    print("Late days:", late_days)
    print("Fine: Rs.", fine)


# show transaction history
def show_transactions():

    db = sqlite3.connect("cryptolabx.db")
    data = db.cursor()

    data.execute("""
        SELECT
            transactions.transaction_id,
            books.title,
            members.name,
            transactions.issue_date,
            transactions.return_date,
            transactions.fine
        FROM transactions
        JOIN books
        ON transactions.book_id = books.book_id
        JOIN members
        ON transactions.mem_id = members.mem_id
    """)

    rows = data.fetchall()

    print("\n--- Transactions ---")

    if len(rows) == 0:

        print("No transactions")

    else:

        for row in rows:

            print("Transaction ID:", row[0])
            print("Book:", row[1])
            print("Member:", row[2])
            print("Issue date:", row[3])
            print("Return date:", row[4])
            print("Fine:", row[5])
            print("-------------------")

    db.close()


# main program
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
    print("8. Show Transactions")
    print("9. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        register_member()

    elif choice == "2":

        add_book()

    elif choice == "3":

        show_members()

    elif choice == "4":

        show_books()

    elif choice == "5":

        search_book()

    elif choice == "6":

        issue_book()

    elif choice == "7":

        return_book()

    elif choice == "8":

        show_transactions()

    elif choice == "9":

        print("Program closed")
        break

    else:

        print("Wrong choice")