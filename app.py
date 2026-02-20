# app.py - Main Flask application for Library Management System
# Run with: python app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from config import BOOKS_PER_PAGE, SECRET_KEY
import database as db

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ---------- Home & Books (Amazon-style grid) ----------

@app.route('/')
def home():
    """Home page - redirects to books listing."""
    return redirect(url_for('books'))


@app.route('/books')
def books():
    """
    Books page: Amazon-style grid of books with search, genre filter,
    availability filter, pagination, and total count.
    """
    page = request.args.get('page', 1, type=int)
    if page < 1:
        page = 1
    search = request.args.get('search', '').strip() or None
    genre = request.args.get('genre', '').strip() or None
    availability = request.args.get('availability', '').strip() or None
    if availability == '':
        availability = None

    offset = (page - 1) * BOOKS_PER_PAGE
    books_list, total = db.get_books(
        search=search,
        genre=genre,
        availability=availability,
        limit=BOOKS_PER_PAGE,
        offset=offset
    )
    genres = db.get_genres()
    total_books_count = db.get_total_books_count()
    total_pages = (total + BOOKS_PER_PAGE - 1) // BOOKS_PER_PAGE if total else 1

    return render_template(
        'books.html',
        books=books_list,
        genres=genres,
        total_books_count=total_books_count,
        total=total,
        page=page,
        total_pages=total_pages,
        search=search or '',
        selected_genre=genre or '',
        selected_availability=availability or ''
    )


# ---------- Add Book ----------

@app.route('/books/add', methods=['GET', 'POST'])
def add_book_page():
    """Add a new book: GET shows form, POST saves to database."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        genre = request.form.get('genre', '').strip()
        quantity = request.form.get('quantity', 1, type=int)
        cover_image_url = request.form.get('cover_image_url', '').strip() or None
        if not title or not author or not genre:
            flash('Please fill in Title, Author, and Genre.', 'error')
            return redirect(url_for('add_book_page'))
        success, message = db.add_book(title, author, genre, quantity, cover_image_url)
        if success:
            flash(message, 'success')
            return redirect(url_for('books'))
        flash(message, 'error')
        return redirect(url_for('add_book_page'))
    genres = db.get_genres()
    return render_template('add_book.html', genres=genres)


# ---------- Remove Book ----------

@app.route('/books/<int:book_id>/remove', methods=['POST'])
def remove_book_route(book_id):
    """Remove a book from the library. Called via form POST (e.g. from book card)."""
    success, message = db.remove_book(book_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(request.referrer or url_for('books'))


@app.route('/books/<int:book_id>/restock', methods=['GET', 'POST'])
def restock_book(book_id):
    """Restock / update quantity: GET shows form, POST updates and redirects to books."""
    book = db.get_book_by_id(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('books'))
    if request.method == 'POST':
        quantity = request.form.get('quantity', 0, type=int)
        success, message = db.update_book_quantity(book_id, quantity)
        if success:
            flash(message, 'success')
            return redirect(url_for('books'))
        flash(message, 'error')
        return redirect(url_for('restock_book', book_id=book_id))
    return render_template('restock.html', book=book)


# ---------- Students ----------

@app.route('/students')
def students():
    """Students page: list of all registered students."""
    students_list = db.get_students()
    return render_template('students.html', students=students_list)


@app.route('/students/add', methods=['GET', 'POST'])
def add_student_page():
    """Add a new student: GET shows form, POST saves to database."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        class_name = request.form.get('class', '').strip()
        email = request.form.get('email', '').strip()
        if not name or not class_name or not email:
            flash('Please fill in Name, Class, and Email.', 'error')
            return redirect(url_for('add_student_page'))
        success, message = db.add_student(name, class_name, email)
        if success:
            flash(message, 'success')
            return redirect(url_for('students'))
        flash(message, 'error')
        return redirect(url_for('add_student_page'))
    return render_template('add_student.html')


# ---------- Issue / Return ----------


# ---------- Issue / Return ----------

@app.route('/issue-return', methods=['GET', 'POST'])
def issue_return():
    """
    Issue/Return page: view records and perform issue/return actions.
    GET: show recent records and form to issue a book.
    POST: handle issue book or return book action.
    """
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'issue':
            book_id = request.form.get('book_id', type=int)
            student_id = request.form.get('student_id', type=int)
            if book_id and student_id:
                success, message = db.issue_book(book_id, student_id)
                if success:
                    flash(message, 'success')
                else:
                    flash(message, 'error')
            else:
                flash('Please select both book and student.', 'error')
            return redirect(url_for('issue_return'))
        elif action == 'return':
            record_id = request.form.get('record_id', type=int)
            if record_id:
                success, message = db.return_book(record_id)
                if success:
                    flash(message, 'success')
                else:
                    flash(message, 'error')
            return redirect(url_for('issue_return'))

    records = db.get_issue_return_records(limit=50)
    students_list = db.get_students()
    # For issue form we need list of available books
    books_list, _ = db.get_books(availability='available', limit=500, offset=0)
    return render_template(
        'issue_return.html',
        records=records,
        students=students_list,
        available_books=books_list
    )


# ---------- Run ----------

if __name__ == '__main__':
    app.run(debug=True, port=5000)
