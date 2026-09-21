# config.py - Database and app configuration
# Change these values according to your MongoDB setup

import os

# ----------------------------
# MongoDB Database Configuration
# ----------------------------
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://127.0.0.1:27017')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'library_db')

# ----------------------------
# Flask Configuration
# ----------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = True

# ----------------------------
# Pagination
# ----------------------------
BOOKS_PER_PAGE = 12  # Number of books per page for listing
