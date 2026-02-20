# config.py - Database and app configuration
# Change these values according to your MySQL setup

import os

# ----------------------------
# MySQL Database Configuration
# ----------------------------
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')          # MySQL host
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')               # MySQL username
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'DbRoot!Secure#2026')  # MySQL password
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'library_db') # Database name

# ----------------------------
# Flask Configuration
# ----------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = True

# ----------------------------
# Pagination
# ----------------------------
BOOKS_PER_PAGE = 12  # Number of books per page for listing
