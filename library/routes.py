from datetime import date
import requests
import json

from library.forms import book_form, member_form, delete_form, return_book_form, borrow_book_form
from flask import render_template, redirect, url_for, flash, request
from library import app, db
from library.models import Member, Book, Transaction


# Renders Home Page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', book_form = book_form(), member_form = member_form())


# Renders Books Page
@app.route('/books', methods=['GET', 'POST'])
def books_page():
    books = Book.query.all()
    form_book = book_form()  # Read books from db
    if form_book.validate_on_submit():  # if no error
        # Create a book in db
        book_to_create = Book(title = book_form().title.data,
                              isbn = book_form().isbn.data,
                              author = book_form().author.data,
                              stock = book_form().stock.data,
                              borrow_stock = book_form().stock.data)
        db.session.add(book_to_create)
        db.session.commit()
        flash('Successfully create a book', category="success")
        return redirect(url_for('books_page'))

    if form_book.errors != {}:  # If there are no errors from the validations
        for err_msg in form_book.errors.values():
            flash(f'There was an error with creating a book: {err_msg}', category='danger')
    
    return render_template('books/books.html', book_form=book_form(), form = delete_form(), books=books)


# Renders Members Page
@app.route('/members', methods=['GET', 'POST'])
def members_page():
    member = Member.query.all() 
    form_member = member_form() # members to read
    if form_member.validate_on_submit():
        # Create a member in db
        member_to_create = Member(name = member_form().name.data,  # add member to db
                                  phone_number = member_form().phone_number.data,
                                  member_name = member_form().member_name.data)
        db.session.add(member_to_create)
        db.session.commit()
        flash('Successfully create a member', category="success")
        return redirect(url_for('members_page'))

    if form_member.errors != {}: # If there are not errors from the validations
        for err_msg in form_member.errors.values():
            flash(f'There was an error with creating a Member: {err_msg}', category = 'danger')
    return render_template('members/members.html', member_form=member_form(), members=member)



@app.route('/transactions')
def transactions_page():
    transaction = Transaction.query.all()
    return render_template('transactions/transactions.html', transactions=transaction)


#Delets a book
@app.route('/delete-book/<book_id>', methods=['GET','POST'])
def delete_book(book_id):
    print(book_id)
    try:
        # finds a book
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        flash("Deleted Successfully", category="success")
    except:
        flash("Error in deletion", category="danger")
    return redirect(url_for('books_page'))


@app.route('/delete-member/<member_id>', methods=['POST'])
def delete_member(member_id):
    try:
        member = Member.query.filter_by(id=member_id).first()
        db.session.delete(member)
        db.session.commit()
        flash("Deleted Successfully", category="success")
    except:
        flash("Error in deletion", category="danger")
    return redirect(url_for('members_page'))


@app.route('/update-book/<book_id>', methods=['GET','POST'])
def update_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    newTitle = request.form.get("title")
    newAuthor = request.form.get("author")
    newIsbn = request.form.get("isbn")
    newStock = request.form.get('stock')
    try:
        if(book.title is not newTitle):
            book.title = newTitle
        if(book.author is not newAuthor):
            book.author = newAuthor
        if(book.isbn is not newIsbn):
            book.isbn = newIsbn
        if(book.stock is not newStock):
            book.stock = newStock
            book.borrow_stock = newStock
        db.session.commit()
        flash("Updated Successfully!", category="success")
    except:
        flash("Failed to update", category="danger")
    return redirect(url_for('books_page'))


@app.route('/update-member/<member_id>', methods=['GET','POST'])
def update_member(member_id):
    member = Member.query.filter_by(id=member_id).first()
    newName = request.form.get("name")
    newNumber = request.form.get("phone_number")
    newMember = request.form.get("member_name")
    try:
        if(member.name is not newName):
            member.name = newName
        if(member.phone_number is not newNumber):
            member.phone_number = newNumber
        if(member.member_name is not newMember):
            member.member_name = newMember
        db.session.commit()
        flash("Updated Successfully!", category="success")
    except:
        flash("Failed to update", category="danger")
    return redirect(url_for('members_page'))


@app.route('/import-from-frappe', methods=['GET','POST'])
def import_books_from_frappe():
    title = request.form.get('title')
    books = []
    url = f"https://frappe.io/api/method/frappe-library?page=1&title={title}"
    books = requests.get(url).json()['message']
    book_list = db.session.query(Book.title).all()
    book_list = list(map(' '.join, book_list))
    author_list = db.session.query(Book.author).all()
    author_list = list(map(' '.join, author_list))
    if len(books) > 0:
        for book in books:
            if(book['title'] not in book_list and book['authors'] not in author_list):
                book_to_create = Book(title=book['title'],  # add book to db
                                  isbn=(book['isbn']),
                                  author=book['authors'],
                                  stock=0,
                                  borrow_stock=0)
                db.session.add(book_to_create)
                db.session.commit()
                flash("succesfully Imported", category="success")

            else:
                continue
    else:
        flash("No response from the API", category="danger")
    return redirect(url_for('books_page'))


@app.route('/borrow-book', methods=['POST'])
def borrow_book():
    member_requested = borrow_book_form().member_name.data()
    book_requested = borrow_book_form().book_name.data()
    if borrow_book_form().validate_on_submit():
        book = Book.query.get(book_requested)
        member = Member.query.get(member_requested)
        member.amount = member.amount - 30
        book.borrow_stock = book.borrow_stock - 1
        book. member = member.id
        borrow_book = Transaction(book = book.title,
                                  member = member.member_name,
                                  type_of_transaction = "borrow",
                                  returned = False,
                                  date= date.today())
        db.session.add(borrow_book)
        db.session.commit()
        flash(f"Issued book to {member_requested}", category='success')
    if borrow_book_form().errors != {}:  # If there are not errors from the validations
        for err_msg in borrow_book_form().errors.values():
            flash(f'There was an error with borrowing book: {err_msg}', category = 'danger')
    return redirect(url_for('transactions_page'))


@app.route('/return-book', methods=['POST'])
def return_book():
    member_requested = return_book_form().member_name.data()
    book_requested = return_book_form().book_name.data()
    paid = return_book_form().paid.data()
    if return_book_form().validate_on_submit():
        transac = Transaction.query.get(book_requested) and Transaction.query.get(member_requested)
        book = Book.query.get(book_requested)
        member = Member.query.get(member_requested)
        member.amount = member.amount - paid
        book.borrow_stock = book.borrow_stock+1
        transac.returned = True
        return_book = Transaction(book = book.id,
                                  member = member.id,
                                  type_of_transaction = "return",
                                  amount = paid,
                                  date= date.today())
        db.session.add(return_book)
        db.session.commit()
        flash(f"Returned book from {member_requested}", category='success')
    if return_book_form().errors != {}:  # If there are not errors from the validations
        for err_msg in return_book_form().errors.values():
            flash(f'There was an error with returning book: {err_msg}', category = 'danger')
    return redirect(url_for('transactions_page'))
# NOTES:

# 1. REMOVE all CamelCase
# 2. Give meaning ful names to functions, classes and variables
# 3. CLEAN code: Indentation, commas etc.
# 4. Download `autopep8`, `pylance` -> VSCode Extension
# Separate `routes` into modules: `member`, `transaction` and `book`
# 5. {% asdf %}
# 6. {% block <kfs> %} # compared to {%block <kfs>%}
        # .. (indentation)
#    {% endbloc %}

# Counting frequency of occurence (uses dictionary)

# my_dict = {} # set() {1, 2, 3}
# trans = []
# for t in trans:
#     if t.type == "borrow":
#         my_dict[t.book_id] = my_dict.get(t.book_id, 0) + 1
#         pass
#     elif "return":
#         pass

# {'xyz': 1}
# {'abc': 1, 'xyz': 1}
# {'abc': 1, 'xyz': 2}
# `key` in max --> documentation
# Lambda
# sorted([(1, 2, 3), (4, 5, 6)])
# max, min, sorted, .sort

# borrowed list => [t for t in borrow_transaction]
# `Transactions` => filters: borrow, return, all
# Sort: date (ASC/DESC), book name (lexiographical), user name (lexiographical)
# Select<option>MEmber 1<options>