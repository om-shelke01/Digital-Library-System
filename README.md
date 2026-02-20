# Library Management System

A **college mini project** that displays books in an **Amazon-style product grid**. Built with **HTML, CSS, Python (Flask), and MySQL**.

## Features

- **Frontend**
  - Grid layout for books (3–4 per row, responsive)
  - Book cover, title, author, genre, and availability
  - Hover effects on book cards
  - Responsive design (mobile and desktop)
  - Navigation: Home, Books, Students, Issue/Return

- **Backend (Flask)**
  - Fetches book data from MySQL
  - Dynamic book grid with search (title/author)
  - Filters by genre and availability
  - Pagination for large lists

- **Database (MySQL)**
  - **books**: Book ID, Title, Author, Genre, Quantity, Cover Image URL
  - **students**: Student ID, Name, Class, Email
  - **issue_return**: Record ID, Book ID, Student ID, Issue Date, Return Date

- **Extra**
  - Unavailable books highlighted (badge + muted style)
  - Total books count on Books page
  - Pagination
  - “Issue Book” and “Return” actions on Issue/Return page

## Project Structure

```
ECOM-WEBSITE/
├── app.py              # Flask application and routes
├── config.py           # Database and app configuration
├── database.py         # MySQL connection and queries
├── requirements.txt    # Python dependencies
├── README.md
├── database/
│   ├── schema.sql      # Create tables
│   └── seed_data.sql   # Sample books, students, records
├── templates/
│   ├── base.html       # Layout and navigation
│   ├── books.html      # Books grid page
│   ├── students.html   # Students list
│   └── issue_return.html
└── static/
    └── css/
        └── style.css   # All styles
```

## Setup

### 1. MySQL

- Install MySQL and create the database and tables:

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p library_db < database/seed_data.sql
```

Or run the contents of `database/schema.sql` and `database/seed_data.sql` in MySQL Workbench or phpMyAdmin.

### 2. Python

- Create a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configuration

- Edit `config.py` and set your MySQL credentials:

  - `MYSQL_HOST` (default: `localhost`)
  - `MYSQL_USER` (default: `root`)
  - `MYSQL_PASSWORD` (default: `''`)
  - `MYSQL_DATABASE` (default: `library_db`)

### 4. Run the app

```bash
python app.py
```

- Open **http://127.0.0.1:5000** in your browser.

## Usage

- **Home / Books**: View all books in a grid. Use the search box (title/author), genre and availability filters, and pagination.
- **Students**: View registered students.
- **Issue/Return**: Issue a book to a student (dropdowns for book and student), and mark returns in the table.

## Tech Stack

- **Frontend**: HTML5, CSS3 (grid, flexbox, responsive)
- **Backend**: Python 3, Flask
- **Database**: MySQL
- **Optional**: Use environment variables for `MYSQL_*` and `SECRET_KEY` in production.

---

*Library Management System — College Mini Project*
