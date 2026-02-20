# database.py - MySQL connection and query helpers
# Handles all database operations for the Library Management System

import mysql.connector
from mysql.connector import Error
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


def get_connection():
    """
    Create and return a MySQL database connection.
    Returns None if connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="DbRoot!Secure#2026",
            database="library_db"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return None


def get_books(search=None, genre=None, availability=None, limit=12, offset=0):
    """
    Fetch books from database with optional search and filters.
    Returns list of book dicts and total count.
    """
    conn = get_connection()
    if not conn:
        return [], 0

    try:
        cursor = conn.cursor(dictionary=True)

        # Build query with optional filters
        where_clauses = []
        params = []

        if search:
            where_clauses.append("(title LIKE %s OR author LIKE %s)")
            params.extend([f"%{search}%", f"%{search}%"])
        if genre:
            where_clauses.append("genre = %s")
            params.append(genre)
        if availability is not None:
            if availability == 'available':
                where_clauses.append("quantity > 0")
            elif availability == 'unavailable':
                where_clauses.append("quantity <= 0")

        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

        # Get total count for pagination
        count_sql = f"SELECT COUNT(*) as total FROM books WHERE {where_sql}"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()['total']

        # Get books with limit and offset
        params.extend([limit, offset])
        books_sql = f"""
            SELECT book_id, title, author, genre, quantity, cover_image_url
            FROM books
            WHERE {where_sql}
            ORDER BY title
            LIMIT %s OFFSET %s
        """
        cursor.execute(books_sql, params)
        books = cursor.fetchall()

        # Add availability flag for frontend
        for book in books:
            book['available'] = book['quantity'] > 0
            book['availability_text'] = 'In Stock' if book['available'] else 'Out of Stock'

        cursor.close()
        conn.close()
        return books, total

    except Error as e:
        print(f"Error fetching books: {e}")
        if conn:
            conn.close()
        return [], 0


def get_book_by_id(book_id):
    """Fetch a single book by ID. Returns None if not found."""
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT book_id, title, author, genre, quantity, cover_image_url FROM books WHERE book_id = %s",
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            book['available'] = book['quantity'] > 0
            book['availability_text'] = 'In Stock' if book['available'] else 'Out of Stock'
        cursor.close()
        conn.close()
        return book
    except Error as e:
        print(f"Error fetching book: {e}")
        if conn:
            conn.close()
        return None


def get_genres():
    """Get list of distinct genres for filter dropdown."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT genre FROM books ORDER BY genre")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [r['genre'] for r in rows]
    except Error as e:
        print(f"Error fetching genres: {e}")
        if conn:
            conn.close()
        return []


def get_total_books_count():
    """Return total number of books in the database."""
    conn = get_connection()
    if not conn:
        return 0
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM books")
        total = cursor.fetchone()['total']
        cursor.close()
        conn.close()
        return total
    except Error as e:
        if conn:
            conn.close()
        return 0


def get_students():
    """Fetch all students for the Students page."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT student_id, name, class, email FROM students ORDER BY name")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return students
    except Error as e:
        print(f"Error fetching students: {e}")
        if conn:
            conn.close()
        return []


def add_student(name, class_name, email):
    """
    Add a new student to the library.
    Returns (success: bool, message: str). class_name is the student's class (e.g. CS-A).
    """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO students (name, class, email) VALUES (%s, %s, %s)",
            (name.strip(), class_name.strip(), email.strip())
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return True, f"Student added successfully. (ID: {new_id})"
    except Error as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, str(e)


def get_issue_return_records(limit=50):
    """Fetch recent issue/return records with book and student details."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.record_id, r.book_id, r.student_id, r.issue_date, r.return_date,
                   b.title AS book_title, s.name AS student_name
            FROM issue_return r
            LEFT JOIN books b ON r.book_id = b.book_id
            LEFT JOIN students s ON r.student_id = s.student_id
            ORDER BY r.issue_date DESC
            LIMIT %s
        """, (limit,))
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records
    except Error as e:
        print(f"Error fetching issue/return records: {e}")
        if conn:
            conn.close()
        return []


def issue_book(book_id, student_id):
    """
    Record a book issue: insert into issue_return and decrement book quantity.
    Returns (success: bool, message: str).
    """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT quantity FROM books WHERE book_id = %s", (book_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, "Book not found."
        if row['quantity'] <= 0:
            conn.close()
            return False, "Book is out of stock."
        cursor.execute(
            "INSERT INTO issue_return (book_id, student_id, issue_date, return_date) VALUES (%s, %s, CURDATE(), NULL)",
            (book_id, student_id)
        )
        cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = %s", (book_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Book issued successfully."
    except Error as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, str(e)


def add_book(title, author, genre, quantity=1, cover_image_url=None):
    """
    Add a new book to the library.
    Returns (success: bool, message: str). On success, message can include the new book_id.
    """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO books (title, author, genre, quantity, cover_image_url) VALUES (%s, %s, %s, %s, %s)",
            (title.strip(), author.strip(), genre.strip(), max(0, int(quantity)), cover_image_url.strip() if cover_image_url else None)
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return True, f"Book added successfully. (ID: {new_id})"
    except Error as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, str(e)


def update_book_quantity(book_id, quantity):
    """
    Update a book's quantity (restock). Use this to set in-stock or out-of-stock.
    Returns (success: bool, message: str).
    """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT book_id, title FROM books WHERE book_id = %s", (book_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, "Book not found."
        qty = max(0, int(quantity))
        cursor.execute("UPDATE books SET quantity = %s WHERE book_id = %s", (qty, book_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, f"Quantity updated for \"{row['title']}\". Now {'in stock' if qty > 0 else 'out of stock'}."
    except Error as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, str(e)


def remove_book(book_id):
    """
    Remove a book from the library. Deletes the book and any related issue/return records (CASCADE).
    Returns (success: bool, message: str).
    """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT book_id, title FROM books WHERE book_id = %s", (book_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, "Book not found."
        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, f"Book removed: \"{row['title']}\"."
    except Error as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, str(e)


def return_book(record_id):
    """
    Record a book return: set return_date and increment book quantity.
    Returns (success: bool, message: str).
    """
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT book_id, return_date FROM issue_return WHERE record_id = %s", (record_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, "Record not found."
        if row['return_date']:
            conn.close()
            return False, "Book already returned."
        cursor.execute("UPDATE issue_return SET return_date = CURDATE() WHERE record_id = %s", (record_id,))
        cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id = %s", (row['book_id'],))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Book returned successfully."
    except Error as e:
        if conn:
            conn.rollback()
            conn.close()
        return False, str(e)
