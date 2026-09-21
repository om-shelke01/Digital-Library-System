# Seed MongoDB with the same sample books, students, and issue records
# as database/seed_data.sql.
#
# Usage (from project root):
#   python database/seed_mongodb.py

import os
import sys
from datetime import datetime

from pymongo import MongoClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MONGO_DB_NAME, MONGO_URI


BOOKS = [
    {
        'book_id': 1,
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'genre': 'Fiction',
        'quantity': 5,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780061120084-L.jpg',
    },
    {
        'book_id': 2,
        'title': '1984',
        'author': 'George Orwell',
        'genre': 'Dystopian',
        'quantity': 3,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg',
    },
    {
        'book_id': 3,
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'genre': 'Fiction',
        'quantity': 4,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg',
    },
    {
        'book_id': 4,
        'title': 'Pride and Prejudice',
        'author': 'Jane Austen',
        'genre': 'Romance',
        'quantity': 6,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780141439518-L.jpg',
    },
    {
        'book_id': 5,
        'title': 'The Catcher in the Rye',
        'author': 'J.D. Salinger',
        'genre': 'Fiction',
        'quantity': 2,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780316769488-L.jpg',
    },
    {
        'book_id': 6,
        'title': "Harry Potter and the Philosopher's Stone",
        'author': 'J.K. Rowling',
        'genre': 'Fantasy',
        'quantity': 8,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780747532699-L.jpg',
    },
    {
        'book_id': 7,
        'title': 'The Hobbit',
        'author': 'J.R.R. Tolkien',
        'genre': 'Fantasy',
        'quantity': 4,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780547928227-L.jpg',
    },
    {
        'book_id': 8,
        'title': 'Fahrenheit 451',
        'author': 'Ray Bradbury',
        'genre': 'Science Fiction',
        'quantity': 3,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9781451673319-L.jpg',
    },
    {
        'book_id': 9,
        'title': 'The Alchemist',
        'author': 'Paulo Coelho',
        'genre': 'Fiction',
        'quantity': 7,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg',
    },
    {
        'book_id': 10,
        'title': 'Animal Farm',
        'author': 'George Orwell',
        'genre': 'Political Satire',
        'quantity': 5,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780451526342-L.jpg',
    },
    {
        'book_id': 11,
        'title': 'The Da Vinci Code',
        'author': 'Dan Brown',
        'genre': 'Thriller',
        'quantity': 4,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780307474278-L.jpg',
    },
    {
        'book_id': 12,
        'title': 'The Lord of the Rings',
        'author': 'J.R.R. Tolkien',
        'genre': 'Fantasy',
        'quantity': 0,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780544003415-L.jpg',
    },
    {
        'book_id': 13,
        'title': 'Clean Code',
        'author': 'Robert C. Martin',
        'genre': 'Technology',
        'quantity': 3,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780132350884-L.jpg',
    },
    {
        'book_id': 14,
        'title': 'Python Crash Course',
        'author': 'Eric Matthes',
        'genre': 'Technology',
        'quantity': 6,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9781593275990-L.jpg',
    },
    {
        'book_id': 15,
        'title': 'Introduction to Algorithms',
        'author': 'CLRS',
        'genre': 'Technology',
        'quantity': 2,
        'cover_image_url': 'https://covers.openlibrary.org/b/isbn/9780262033848-L.jpg',
    },
]

STUDENTS = [
    {'student_id': 1, 'name': 'Alice Johnson', 'class': 'CS-A', 'email': 'alice.johnson@college.edu'},
    {'student_id': 2, 'name': 'Bob Smith', 'class': 'CS-B', 'email': 'bob.smith@college.edu'},
    {'student_id': 3, 'name': 'Carol Williams', 'class': 'IT-A', 'email': 'carol.williams@college.edu'},
    {'student_id': 4, 'name': 'David Brown', 'class': 'CS-A', 'email': 'david.brown@college.edu'},
    {'student_id': 5, 'name': 'Eva Davis', 'class': 'IT-B', 'email': 'eva.davis@college.edu'},
    {'student_id': 6, 'name': 'Frank Miller', 'class': 'CS-B', 'email': 'frank.miller@college.edu'},
]

ISSUE_RETURN = [
    {'record_id': 1, 'book_id': 1, 'student_id': 1, 'issue_date': datetime(2025, 1, 10), 'return_date': datetime(2025, 1, 25)},
    {'record_id': 2, 'book_id': 2, 'student_id': 2, 'issue_date': datetime(2025, 2, 1), 'return_date': None},
    {'record_id': 3, 'book_id': 3, 'student_id': 3, 'issue_date': datetime(2025, 2, 5), 'return_date': None},
    {'record_id': 4, 'book_id': 5, 'student_id': 1, 'issue_date': datetime(2025, 2, 10), 'return_date': None},
]


def seed():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client[MONGO_DB_NAME]
    now = datetime.now()

    db.books.delete_many({})
    db.students.delete_many({})
    db.issue_return.delete_many({})
    db.counters.delete_many({})

    books = [{**book, 'created_at': now} for book in BOOKS]
    students = [{**student, 'created_at': now} for student in STUDENTS]
    records = [{**record, 'created_at': now} for record in ISSUE_RETURN]

    db.books.insert_many(books)
    db.students.insert_many(students)
    db.issue_return.insert_many(records)
    db.counters.insert_many([
        {'_id': 'book_id', 'seq': max(b['book_id'] for b in BOOKS)},
        {'_id': 'student_id', 'seq': max(s['student_id'] for s in STUDENTS)},
        {'_id': 'record_id', 'seq': max(r['record_id'] for r in ISSUE_RETURN)},
    ])

    db.books.create_index('book_id', unique=True)
    db.books.create_index('title')
    db.books.create_index('author')
    db.books.create_index('genre')
    db.students.create_index('student_id', unique=True)
    db.issue_return.create_index('record_id', unique=True)
    db.issue_return.create_index('book_id')
    db.issue_return.create_index('student_id')

    print(f"Seeded MongoDB database '{MONGO_DB_NAME}' at {MONGO_URI}")
    print(f"  books: {db.books.count_documents({})}")
    print(f"  students: {db.students.count_documents({})}")
    print(f"  issue_return: {db.issue_return.count_documents({})}")
    client.close()


if __name__ == '__main__':
    seed()
