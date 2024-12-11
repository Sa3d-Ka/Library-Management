# Library Management System with Python

## Objective
Develop a Python-based library management system to help librarians manage books, loans, and users efficiently.

---

## Features

### 1. **Book Management**
- **`addBook(title, author, isbn, quantity)`**: Add a new book.
- **`removeBook(isbn)`**: Remove a book by ISBN.

### 2. **Loan Management**
- **`borrowBook(isbn, user)`**: Borrow a book and update quantity.
- **`returnBook(isbn, user)`**: Return a book and update quantity.
- **`calculateFine(expectedDate, actualDate)`**: Calculate fines for overdue returns (5 Unite/day).

### 3. **Book Search**
- **`searchBooks(keyword)`**: Search books by title or author.

### 4. **Statistics**
- **`bookStatistics()`**: Show total books, borrowed books, and available books.

### 5. **User Management**
- **`addUser(lastName, firstName, cardNumber)`**: Add a new user.
- **`removeUser(cardNumber)`**: Remove a user by card number.

---

## Author
Saad Kanani



