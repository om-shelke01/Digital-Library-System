# database.py - MongoDB connection and query helpers
# Handles all database operations for the Library Management System

import re
from datetime import date, datetime

from pymongo import ASCENDING, DESCENDING, MongoClient, ReturnDocument
from pymongo.errors import PyMongoError

from config import MONGO_DB_NAME, MONGO_URI

_client = None


def get_client():
    """Create and return a shared MongoDB client."""
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return _client


def get_db():
    """Return the library_db database."""
    return get_client()[MONGO_DB_NAME]


def get_connection():
    """
    Check MongoDB connectivity.
    Returns the database object, or None if the connection fails.
    """
    try:
        client = get_client()
        client.admin.command('ping')
        return get_db()
    except PyMongoError as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def init_db():
    """Create indexes used for search, filters, and unique integer IDs."""
    db = get_connection()
    if db is None:
        return
    db.books.create_index('book_id', unique=True)
    db.books.create_index('title')
    db.books.create_index('author')
    db.books.create_index('genre')
    db.students.create_index('student_id', unique=True)
    db.issue_return.create_index('record_id', unique=True)
    db.issue_return.create_index('book_id')
    db.issue_return.create_index('student_id')


def next_id(sequence_name):
    """Return the next integer ID for books, students, or issue records."""
    db = get_db()
    doc = db.counters.find_one_and_update(
        {'_id': sequence_name},
        {'$inc': {'seq': 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(doc['seq'])


def _today():
    now = datetime.now()
    return datetime(now.year, now.month, now.day)


def _as_date(value):
    """Convert MongoDB datetimes to date objects so templates match MySQL output."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return value


def _book_view(doc):
    if not doc:
        return None
    book = {
        'book_id': doc.get('book_id'),
        'title': doc.get('title'),
        'author': doc.get('author'),
        'genre': doc.get('genre'),
        'quantity': int(doc.get('quantity') or 0),
        'cover_image_url': doc.get('cover_image_url'),
    }
    book['available'] = book['quantity'] > 0
    book['availability_text'] = 'In Stock' if book['available'] else 'Out of Stock'
    return book


def _student_view(doc):
    if not doc:
        return None
    return {
        'student_id': doc.get('student_id'),
        'name': doc.get('name'),
        'class': doc.get('class'),
        'email': doc.get('email'),
    }


def get_books(search=None, genre=None, availability=None, limit=12, offset=0):
    """
    Fetch books from database with optional search and filters.
    Returns list of book dicts and total count.
    """
    db = get_connection()
    if db is None:
        return [], 0

    try:
        query = {}
        clauses = []

        if search:
            safe = re.escape(search)
            clauses.append({
                '$or': [
                    {'title': {'$regex': safe, '$options': 'i'}},
                    {'author': {'$regex': safe, '$options': 'i'}},
                ]
            })
        if genre:
            clauses.append({'genre': genre})
        if availability == 'available':
            clauses.append({'quantity': {'$gt': 0}})
        elif availability == 'unavailable':
            clauses.append({'quantity': {'$lte': 0}})

        if len(clauses) == 1:
            query = clauses[0]
        elif clauses:
            query = {'$and': clauses}

        total = db.books.count_documents(query)
        cursor = (
            db.books.find(query)
            .sort('title', ASCENDING)
            .skip(int(offset))
            .limit(int(limit))
        )
        books = [_book_view(doc) for doc in cursor]
        return books, total
    except PyMongoError as e:
        print(f"Error fetching books: {e}")
        return [], 0


def get_book_by_id(book_id):
    """Fetch a single book by ID. Returns None if not found."""
    db = get_connection()
    if db is None:
        return None
    try:
        doc = db.books.find_one({'book_id': int(book_id)})
        return _book_view(doc)
    except (PyMongoError, TypeError, ValueError) as e:
        print(f"Error fetching book: {e}")
        return None


def get_genres():
    """Get list of distinct genres for filter dropdown."""
    db = get_connection()
    if db is None:
        return []
    try:
        return sorted(g for g in db.books.distinct('genre') if g)
    except PyMongoError as e:
        print(f"Error fetching genres: {e}")
        return []


def get_total_books_count():
    """Return total number of books in the database."""
    db = get_connection()
    if db is None:
        return 0
    try:
        return db.books.count_documents({})
    except PyMongoError:
        return 0


def get_students():
    """Fetch all students for the Students page."""
    db = get_connection()
    if db is None:
        return []
    try:
        cursor = db.students.find({}).sort('name', ASCENDING)
        return [_student_view(doc) for doc in cursor]
    except PyMongoError as e:
        print(f"Error fetching students: {e}")
        return []


def add_student(name, class_name, email):
    """
    Add a new student to the library.
    Returns (success: bool, message: str). class_name is the student's class (e.g. CS-A).
    """
    db = get_connection()
    if db is None:
        return False, "Database connection failed."
    try:
        new_id = next_id('student_id')
        db.students.insert_one({
            'student_id': new_id,
            'name': name.strip(),
            'class': class_name.strip(),
            'email': email.strip(),
            'created_at': datetime.now(),
        })
        return True, f"Student added successfully. (ID: {new_id})"
    except PyMongoError as e:
        return False, str(e)


def get_issue_return_records(limit=50):
    """Fetch recent issue/return records with book and student details."""
    db = get_connection()
    if db is None:
        return []
    try:
        pipeline = [
            {'$sort': {'issue_date': DESCENDING, 'record_id': DESCENDING}},
            {'$limit': int(limit)},
            {
                '$lookup': {
                    'from': 'books',
                    'localField': 'book_id',
                    'foreignField': 'book_id',
                    'as': 'book',
                }
            },
            {
                '$lookup': {
                    'from': 'students',
                    'localField': 'student_id',
                    'foreignField': 'student_id',
                    'as': 'student',
                }
            },
        ]
        records = []
        for doc in db.issue_return.aggregate(pipeline):
            book = doc.get('book') or []
            student = doc.get('student') or []
            records.append({
                'record_id': doc.get('record_id'),
                'book_id': doc.get('book_id'),
                'student_id': doc.get('student_id'),
                'issue_date': _as_date(doc.get('issue_date')),
                'return_date': _as_date(doc.get('return_date')),
                'book_title': book[0].get('title') if book else None,
                'student_name': student[0].get('name') if student else None,
            })
        return records
    except PyMongoError as e:
        print(f"Error fetching issue/return records: {e}")
        return []


def issue_book(book_id, student_id):
    """
    Record a book issue: insert into issue_return and decrement book quantity.
    Returns (success: bool, message: str).
    """
    db = get_connection()
    if db is None:
        return False, "Database connection failed."
    try:
        book_id = int(book_id)
        student_id = int(student_id)
        student = db.students.find_one({'student_id': student_id})
        if not student:
            return False, "Student not found."

        updated = db.books.find_one_and_update(
            {'book_id': book_id, 'quantity': {'$gt': 0}},
            {'$inc': {'quantity': -1}},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            book = db.books.find_one({'book_id': book_id})
            if not book:
                return False, "Book not found."
            return False, "Book is out of stock."

        try:
            db.issue_return.insert_one({
                'record_id': next_id('record_id'),
                'book_id': book_id,
                'student_id': student_id,
                'issue_date': _today(),
                'return_date': None,
                'created_at': datetime.now(),
            })
        except PyMongoError as e:
            db.books.update_one({'book_id': book_id}, {'$inc': {'quantity': 1}})
            return False, str(e)
        return True, "Book issued successfully."
    except (PyMongoError, TypeError, ValueError) as e:
        return False, str(e)


def add_book(title, author, genre, quantity=1, cover_image_url=None):
    """
    Add a new book to the library.
    Returns (success: bool, message: str). On success, message can include the new book_id.
    """
    db = get_connection()
    if db is None:
        return False, "Database connection failed."
    try:
        new_id = next_id('book_id')
        db.books.insert_one({
            'book_id': new_id,
            'title': title.strip(),
            'author': author.strip(),
            'genre': genre.strip(),
            'quantity': max(0, int(quantity)),
            'cover_image_url': cover_image_url.strip() if cover_image_url else None,
            'created_at': datetime.now(),
        })
        return True, f"Book added successfully. (ID: {new_id})"
    except (PyMongoError, TypeError, ValueError) as e:
        return False, str(e)


def update_book_quantity(book_id, quantity):
    """
    Update a book's quantity (restock). Use this to set in-stock or out-of-stock.
    Returns (success: bool, message: str).
    """
    db = get_connection()
    if db is None:
        return False, "Database connection failed."
    try:
        book_id = int(book_id)
        row = db.books.find_one({'book_id': book_id})
        if not row:
            return False, "Book not found."
        qty = max(0, int(quantity))
        db.books.update_one({'book_id': book_id}, {'$set': {'quantity': qty}})
        return True, f"Quantity updated for \"{row['title']}\". Now {'in stock' if qty > 0 else 'out of stock'}."
    except (PyMongoError, TypeError, ValueError) as e:
        return False, str(e)


def remove_book(book_id):
    """
    Remove a book from the library. Deletes the book and any related issue/return records (CASCADE).
    Returns (success: bool, message: str).
    """
    db = get_connection()
    if db is None:
        return False, "Database connection failed."
    try:
        book_id = int(book_id)
        row = db.books.find_one({'book_id': book_id})
        if not row:
            return False, "Book not found."
        db.issue_return.delete_many({'book_id': book_id})
        db.books.delete_one({'book_id': book_id})
        return True, f"Book removed: \"{row['title']}\"."
    except (PyMongoError, TypeError, ValueError) as e:
        return False, str(e)


def return_book(record_id):
    """
    Record a book return: set return_date and increment book quantity.
    Returns (success: bool, message: str).
    """
    db = get_connection()
    if db is None:
        return False, "Database connection failed."
    try:
        record_id = int(record_id)
        row = db.issue_return.find_one_and_update(
            {'record_id': record_id, 'return_date': None},
            {'$set': {'return_date': _today()}},
            return_document=ReturnDocument.BEFORE,
        )
        if not row:
            existing = db.issue_return.find_one({'record_id': record_id})
            if not existing:
                return False, "Record not found."
            return False, "Book already returned."
        db.books.update_one({'book_id': row['book_id']}, {'$inc': {'quantity': 1}})
        return True, "Book returned successfully."
    except (PyMongoError, TypeError, ValueError) as e:
        return False, str(e)
