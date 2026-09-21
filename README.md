# MyLibrary (Flask + MongoDB)

**MyLibrary** is a college library management website built with **Flask and MongoDB**.

The site name is **MyLibrary**. The navbar and footer use an **OM** logo mark (the initials in the gold square next to the name), with the same size, color, and position as before.

This project is a **college mini project** for managing a small academic library. It lets you manage books, register students, and issue or return books, while keeping stock up to date.

---

## Key Features

### Books Management
- View books in a responsive catalog grid
- Search books by title or author
- Filter by genre and availability
- Pagination with total book count
- Add, restock, or remove books

### Students Management
- Register new students
- View student list
- Store student details (name, class, email)

### Issue and Return
- Issue books to registered students
- Return issued books
- Automatic stock update on issue/return
- Prevent issuing books when stock is unavailable

---

## Branding

- Project name: **MyLibrary**
- Logo mark: **OM** (navbar and footer)
- Logo style is defined in `static/css/style.css` (class `.nav-mark`)

---

## Tech Stack

- Frontend: HTML5, CSS3 (Grid and Flexbox, responsive UI), JavaScript
- Backend: Python, Flask
- Database: MongoDB (PyMongo)

---

## Project Structure

```
Digital-Library-System/
├── app.py
├── config.py
├── database.py
├── requirements.txt
├── README.md
├── PROJECT_EXPLANATION_FOR_TEACHERS.txt
├── database/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── seed_mongodb.py
├── templates/
│   ├── base.html
│   ├── books.html
│   ├── restock.html
│   ├── students.html
│   ├── add_book.html
│   ├── add_student.html
│   └── issue_return.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

---

## Installation and Setup

### Database Setup (MongoDB)

1. Start MongoDB locally (default: `mongodb://127.0.0.1:27017`).
2. Install Python dependencies, then seed sample data:

```
python database/seed_mongodb.py
```

This creates the `library_db` database with `books`, `students`, and `issue_return` collections.

The original MySQL files (`database/schema.sql` and `database/seed_data.sql`) are kept for reference and are not used by the running app.

---

### Python Setup

Create and activate a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

### Configuration (Optional)

You can configure the application using environment variables:

- MONGO_URI
- MONGO_DB_NAME
- SECRET_KEY

If these are not set, default values from `config.py` will be used.

---

## Running the Application

```
python app.py
```

Open the application in a browser at:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Author and Academic Details

- Student Name: Om Shelke
- College: Jijamata College of Science and Arts, Bhende
- Course: Second Year BCS (Mini Project)

---

## Academic Disclaimer

This project is created for educational purposes as a college mini project.  
It is not intended for production use without proper security improvements such as authentication, input validation, and secure configuration.

---

## Future Enhancements

- Admin or librarian authentication
- Book reservation system
- Fine calculation for late returns
- Export reports (CSV or PDF)
