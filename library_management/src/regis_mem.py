import sqlite3
from datetime import datetime
from database import initialize_database, get_connection


def register_member():
    name = input("Enter member name: ")
    email = input("Enter email: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO members (name, email) VALUES (?, ?)",
        (name, email)
    )

    connection.commit()
    connection.close()

    print("Member registered successfully.")


def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (title, author)
    )

    connection.commit()
    connection.close()

    print("Book added successfully.")