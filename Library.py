import random
from datetime import datetime
import csv

books = {}
loans = {}
users = {}

def main_program():
    while True:
        print(f"{'-'*15} Main Menu {'-'*15}")
        print("1. Book Management")
        print("2. Loan Management")
        print("3. Book Search")
        print("4. Book Statistics")
        print("5. User Management")
        print("6. Exit")
        print('-' * 40)
        choice = input("Enter your choice: ")
        if choice == '1':
            manage_books()
        elif choice == '2':
            manage_loans()
        elif choice == '3':
            search_books()
        elif choice == '4':
            book_statistics()
        elif choice == '5':
            manage_users()
        elif choice == '6':
            break
        else:
            print("Invalid choice")

def generate_isbn13():
    prefix = random.choice(["978", "979"])
    registration_group = str(random.randint(0, 9))
    registrant = str(random.randint(100, 9999))
    publication = str(random.randint(100, 99999))
    isbn_without_check = prefix + registration_group + registrant + publication
    check_digit = calculate_check_digit(isbn_without_check)
    return isbn_without_check + str(check_digit)

def calculate_check_digit(isbn_without_check):
    total = 0
    for i, digit in enumerate(isbn_without_check):
        total += int(digit) if i % 2 == 0 else 3 * int(digit)
    remainder = total % 10
    return 0 if remainder == 0 else 10 - remainder

# ==================== Book Management ==================
def manage_books():
    while True:
        print(f"{'-'*10} Book Management {'-'*10}")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Exit")
        print('-' * 30)
        choice = input("Enter your choice: ")
        if choice == '1':
            add_book()
        elif choice == '2':
            remove_book()
        elif choice == '3':
            break
        else:
            print("Invalid choice")

def add_book():
    title = input("Enter book title: ").title().strip()
    author = input("Enter book author: ").title().strip()
    quantity = int(input("Enter book quantity: "))
    isbn = generate_isbn13()
    print(f"Generated ISBN: {isbn}")
    if isbn in books:
        print(f"A book with ISBN {isbn} already exists.")
        return
    books[isbn] = {
        "Title": title,
        "Author": author,
        "Quantity": quantity
    }
    print(f"Book '{title}' added successfully.")
    Save_Books()

def remove_book():
    isbn = input("Enter ISBN of the book to remove: ")
    if isbn not in books:
        print(f"Book with ISBN {isbn} does not exist.")
        return
    del books[isbn]
    print(f"Book with ISBN {isbn} removed successfully.")
    Save_Books()

# ==================== Loan Management ==================
def manage_loans():
    while True:
        print(f"{'-'*10} Loan Management {'-'*10}")
        print("1. Borrow Book")
        print("2. Return Book")
        print("3. Calculate Fine")
        print("4. Exit")
        print('-' * 30)
        choice = input("Enter your choice: ")
        if choice == '1':
            borrow_book()
        elif choice == '2':
            return_book()
        elif choice == '3':
            calculate_fine()
        elif choice == '4':
            break
        else:
            print("Invalid choice")

def borrow_book():
    user_id = input("Enter user ID: ")
    if user_id not in users:
        print("User does not exist")
        return
    isbn = input("Enter book ISBN: ")
    if isbn not in books:
        print(f"Book with ISBN {isbn} does not exist.")
        return
    if books[isbn]['Quantity'] <= 0:
        print(f"Book '{books[isbn]['Title']}' is not currently available.")
        return
    loans[user_id] = isbn
    books[isbn]['Quantity'] -= 1
    print(f"Book '{books[isbn]['Title']}' borrowed successfully by user {user_id}.")
    Save_Books()
    Save_Loans()

def return_book():
    user_id = input("Enter user ID: ")
    isbn = input("Enter book ISBN: ")
    if user_id not in loans:
        print("No loan record found for this user.")
        return
    del loans[user_id]
    books[isbn]['Quantity'] += 1
    print(f"Book with ISBN {isbn} returned successfully.")
    Save_Books()
    Save_Loans()

def calculate_fine():
    expected_date = input("Enter expected return date (DD/MM/YYYY): ")
    actual_date = input("Enter actual return date (DD/MM/YYYY): ")
    expected = datetime.strptime(expected_date, "%d/%m/%Y")
    actual = datetime.strptime(actual_date, "%d/%m/%Y")
    delay = (actual - expected).days
    if delay > 0:
        fine = delay * 5
        print(f"Late by: {delay} days")
        print(f"Fine: {fine} MAD")
    else:
        print("No delay, no fine.")

# ==================== Book Search ==================
def search_books():
    results = []
    keyword = input("Enter a keyword to search: ")
    for isbn, details in books.items():
        if keyword.lower() in details['Title'].lower() or keyword.lower() in details['Author'].lower():
            results.append(details)
    if results:
        print("Search Results:")
        for book in results:
            print(f"Title: {book['Title']}, Author: {book['Author']}, Quantity: {book['Quantity']}")
    else:
        print("No books found for the given keyword.")

# ==================== Book Statistics ==================
def book_statistics():
    available_books = 0
    total_books = len(books)
    total_loans = len(loans)
    for info in books.values():
        if info['Quantity'] > 0:
            available_books += 1
    print("=== Statistics ===")
    print(f"Total books: {total_books}")
    print(f"Borrowed books: {total_loans}")
    print(f"Available books: {available_books}")

# ==================== User Management ==================
def manage_users():
    while True:
        print(f"{'-'*10} User Management {'-'*10}")
        print("1. Add User")
        print("2. Remove User")
        print("3. Exit")
        print('-' * 30)
        choice = input("Enter your choice: ")
        if choice == '1':
            add_user()
        elif choice == '2':
            remove_user()
        elif choice == '3':
            break
        else:
            print("Invalid choice")

def add_user():
    last_name = input("Enter last name: ").capitalize()
    first_name = input("Enter first name: ").capitalize()
    user_id = input("Enter user ID: ")
    if user_id in users:
        print(f"A user with ID {user_id} already exists.")
        return
    users[user_id] = {
        "Last Name": last_name,
        "First Name": first_name
    }
    print(f"User '{last_name} {first_name}' added successfully.")
    Save_Users()

def remove_user():
    user_id = input("Enter user ID to remove: ")
    if user_id not in users:
        print("User does not exist")
        return
    del users[user_id]
    print(f"User with ID '{user_id}' removed successfully.")
    Save_Users()
#============================================================

#==================== Save Data to CSV ==================
def Save_Books():
    with open('books.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Author", "ISBN", "Quantity"])

        for isbn, info in books.items():
            writer.writerow([info['Title'], info['Author'], isbn, info['Quantity']])

def Save_Loans():
    with open('loans.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["CIN", "ISBN"])

        for cin, isbn in loans.items():
            writer.writerow([cin, isbn])

def Save_Users():
    with open('users.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Surname", "CIN"])

        for cin, info in users.items():
            writer.writerow([info['Name'], info['Surname'], cin])
#====================================================================

#==================== Load Data from CSV ==================
def Load_Data():
    with open('books.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                title, author, isbn, quantity = row
                books[isbn] = {
                    "Title": title,
                    "Author": author,
                    "Quantity": int(quantity)
                }
            print("Books loaded successfully.")

    with open('loans.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cin, isbn = row
            loans[cin] = isbn
        print("Loans loaded successfully.")

    with open('users.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            name, surname, cin = row
            users[cin] = {
                "Name": name,
                "Surname": surname
            }
        print("Users loaded successfully.")  

#====================================================================

Load_Data()
main_program()
