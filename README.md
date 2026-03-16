# Academic Digital Library System (Flask + MySQL)

A **college mini project** for managing a small academic library. The system allows you to **view books**, **register students**, and **issue/return books** with stock tracking.

## Project overview

- **Books module**: responsive book grid, search (title/author), filter by class/semester and availability, pagination, total count
- **Inventory actions**: restock/update quantity, remove book
- **Students module**: list and add students (name, class, email)
- **Issue/Return module**: issue a book to a student, record returns, and update stock automatically

## Tech stack

- **Frontend**: HTML5, CSS3 (grid + flex, responsive)
- **Backend**: Python, Flask
- **Database**: MySQL

## Folder structure

```
Digital-Library-System/
├── app.py                           # Flask routes + page rendering
├── config.py                        # App/database configuration (env defaults)
├── database.py                      # MySQL connection + query helpers
├── requirements.txt                 # Python dependencies
├── README.md
├── PROJECT_EXPLANATION_FOR_TEACHERS.txt
├── database/
│   ├── schema.sql                   # Create DB + tables + indexes
│   └── seed_data.sql                # Sample books/students/records
├── templates/
│   ├── base.html
│   ├── books.html
│   ├── restock.html
│   ├── students.html
│   ├── add_book.html
│   ├── add_student.html
│   └── issue_return.html
└── static/
    └── css/
        └── style.css
```

## Installation

### 1) Database setup (MySQL)

Run the schema and seed scripts:

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p library_db < database/seed_data.sql
```

You can also run `database/schema.sql` and `database/seed_data.sql` in MySQL Workbench / phpMyAdmin.

### 2) Python setup

Create and activate a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3) Configuration (optional)

You can configure MySQL and Flask settings using environment variables:

- `MYSQL_HOST`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`
- `SECRET_KEY`

If you do not set them, defaults from `config.py` are used.

## How to run

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## Screenshots (placeholders)

- Home / Books page: `docs/screenshots/books.png`
- Students page: `docs/screenshots/students.png`
- Issue/Return page: `docs/screenshots/issue_return.png`
- Restock page: `docs/screenshots/restock.png`

## Author

- **Om Shelke** (Lead Developer & Designer)  
- **Project Guide**: Prof. Gholap Sir  
- **College**: Jijamata College of Science and Arts, Bhende

## Academic disclaimer

This project is created **for educational purposes** as a college mini project.  
It is **not intended for production use** without security hardening (e.g., secrets management, input validation, and proper logging).
