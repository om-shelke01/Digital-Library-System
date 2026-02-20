-- Seed data for Library Management System
-- Run after schema.sql: mysql -u root -p library_db < database/seed_data.sql

USE library_db;

-- Sample books with cover image URLs (using placeholder image service)
INSERT INTO books (title, author, genre, quantity, cover_image_url) VALUES
('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 5, 'https://covers.openlibrary.org/b/isbn/9780061120084-L.jpg'),
('1984', 'George Orwell', 'Dystopian', 3, 'https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg'),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 4, 'https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg'),
('Pride and Prejudice', 'Jane Austen', 'Romance', 6, 'https://covers.openlibrary.org/b/isbn/9780141439518-L.jpg'),
('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 2, 'https://covers.openlibrary.org/b/isbn/9780316769488-L.jpg'),
('Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 'Fantasy', 8, 'https://covers.openlibrary.org/b/isbn/9780747532699-L.jpg'),
('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 4, 'https://covers.openlibrary.org/b/isbn/9780547928227-L.jpg'),
('Fahrenheit 451', 'Ray Bradbury', 'Science Fiction', 3, 'https://covers.openlibrary.org/b/isbn/9781451673319-L.jpg'),
('The Alchemist', 'Paulo Coelho', 'Fiction', 7, 'https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg'),
('Animal Farm', 'George Orwell', 'Political Satire', 5, 'https://covers.openlibrary.org/b/isbn/9780451526342-L.jpg'),
('The Da Vinci Code', 'Dan Brown', 'Thriller', 4, 'https://covers.openlibrary.org/b/isbn/9780307474278-L.jpg'),
('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 0, 'https://covers.openlibrary.org/b/isbn/9780544003415-L.jpg'),
('Clean Code', 'Robert C. Martin', 'Technology', 3, 'https://covers.openlibrary.org/b/isbn/9780132350884-L.jpg'),
('Python Crash Course', 'Eric Matthes', 'Technology', 6, 'https://covers.openlibrary.org/b/isbn/9781593275990-L.jpg'),
('Introduction to Algorithms', 'CLRS', 'Technology', 2, 'https://covers.openlibrary.org/b/isbn/9780262033848-L.jpg');

-- Sample students
INSERT INTO students (name, class, email) VALUES
('Alice Johnson', 'CS-A', 'alice.johnson@college.edu'),
('Bob Smith', 'CS-B', 'bob.smith@college.edu'),
('Carol Williams', 'IT-A', 'carol.williams@college.edu'),
('David Brown', 'CS-A', 'david.brown@college.edu'),
('Eva Davis', 'IT-B', 'eva.davis@college.edu'),
('Frank Miller', 'CS-B', 'frank.miller@college.edu');

-- Sample issue/return records (some returned, some not)
INSERT INTO issue_return (book_id, student_id, issue_date, return_date) VALUES
(1, 1, '2025-01-10', '2025-01-25'),
(2, 2, '2025-02-01', NULL),
(3, 3, '2025-02-05', NULL),
(5, 1, '2025-02-10', NULL);
