# internal imports
from library.forms import book_form, member_form, return_book_form, borrow_book_form
from library import app, db

# external imports 
import requests
import json

from datetime import date
from library.forms import book_form, return_book_form, borrow_book_form
from flask import render_template, redirect, url_for, flash, request
from library.models import Book, Member, Transaction
from sqlalchemy import and_


# Renders Home Page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', book_form = book_form(), member_form = member_form(), borrow_form = borrow_book_form(), return_form = return_book_form())



# -------------------------------------Book Routes------------------------------

# Renders book page
@app.route('/books', methods=['GET','POST'])
def books_page():
    # reads books from db
    books = Book.query.all()
    form_book = book_form() 

    # if no validation error while creating book
    if form_book.validate_on_submit():  
        book_to_create = Book(title = book_form().title.data,
                              isbn = book_form().isbn.data,
                              author = book_form().author.data,
                              stock = book_form().stock.data,
                              borrow_stock = book_form().stock.data)
        db.session.add(book_to_create)
        db.session.commit()
        flash('Successfully create a book', category="success")
        return redirect(url_for('books_page'))

    # if error occurs
    if form_book.errors != {}:
        for err_msg in form_book.errors.values():
            flash(f'There was an error with creating a book: {err_msg}', category='danger')
    
    return render_template('books/books.html', book_form=book_form(), books=books, length = len(books), borrow_form = borrow_book_form(), return_form = return_book_form())


# deletes a book
@app.route('/delete-book/<book_id>', methods=['POST'])
def delete_book(book_id):
    try:
        # reads the requested book
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        flash("Deleted Successfully", category="success")

    except:
        flash("Error in deletion", category="danger")

    return redirect(url_for('books_page'))


# updates a book
@app.route('/update-book/<book_id>', methods=['POST'])
def update_book(book_id):
    # reads requested book from db
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


# imports books from Frappe API with given title
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

    # if books are succesfully imported
    if len(books) > 0:
        for book in books:
            # if no duplicate book is found
            if(book['title'] not in book_list and book['authors'] not in author_list):
                book_to_create = Book(title=book['title'], 
                                  isbn=(book['isbn']),
                                  author=book['authors'],
                                  stock=1,
                                  borrow_stock=1)
                db.session.add(book_to_create)
                db.session.commit()
            #skips when a duplicate is found
            else:
                continue
        flash("succesfully Imported", category="success")
    #if error in importing the books
    else:
        flash("No response from the API", category="danger")

    return redirect(url_for('books_page'))



# -------------------------------------Member Routes------------------------------

# Renders member page
@app.route('/members', methods=['GET', 'POST'])
def members_page():
    # read members from db
    member = Member.query.all() 

    form_member = member_form() 

    # if no validation error in creating a member
    if form_member.validate_on_submit():
        # creates a member in db
        member_to_create = Member(name = member_form().name.data,
                                  phone_number = member_form().phone_number.data,
                                  member_name = member_form().member_name.data)
        db.session.add(member_to_create)
        db.session.commit()

        flash('Successfully create a member', category="success")
        return redirect(url_for('members_page'))
    
    # if validation error occured
    if form_member.errors != {}: # If there are not errors from the validations
        for err_msg in form_member.errors.values():
            flash(f'There was an error with creating a Member: {err_msg}', category = 'danger')
    return render_template('members/members.html', member_form=form_member, members=member, length = len(member), borrow_form = borrow_book_form(), return_form = return_book_form())


# deletes a member
@app.route('/delete-member/<member_id>', methods=['POST'])
def delete_member(member_id):
    try:
        # reads requested member from db
        member = Member.query.filter_by(id=member_id).first()
        db.session.delete(member)
        db.session.commit()
        flash("Deleted Successfully", category="success")

    except:
        flash("Error in deletion", category="danger")

    return redirect(url_for('members_page'))



# updates a member
@app.route('/update-member/<member_id>', methods=['GET','POST'])
def update_member(member_id):
    # reads requested member from db
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



# -------------------------------------Transaction Routes------------------------------

@app.route('/transactions')
def transactions_page():
    transaction = Transaction.query.all()
    return render_template('transactions/transactions.html', transactions=transaction, length=len(transaction), borrow_form = borrow_book_form(), return_form = return_book_form())


@app.route('/borrow-book', methods=['POST'])
def borrow_book():
    member_requested = borrow_book_form().member_name.data
    book_requested = borrow_book_form().book_name.data
    borrow_form = borrow_book_form()
    if borrow_form.validate_on_submit():
        book = Book.query.filter_by(title = book_requested).first()
        member = Member.query.filter_by(member_name = member_requested).first()
        member.amount = member.amount - 30
        print(member.amount)
        book.borrow_stock = book.borrow_stock - 1
        book.member = book.member + 1
        borrow_book = Transaction(book = book.id,
                                  book_name = book.title,
                                  member = member.member_name,
                                  type_of_transaction = "borrow",
                                  returned = False,
                                  amount = 0,
                                  date= date.today())
        db.session.add(borrow_book)
        db.session.commit()
        flash(f"Issued book to {member_requested}", category='success')
    if borrow_form.errors != {}:  # If there are not errors from the validations
        for err_msg in borrow_form.errors.values():
            flash(f'There was an error with borrowing book: {err_msg}', category = 'danger')
    return redirect(request.referrer)


@app.route('/return-book', methods=['POST'])
def return_book():
    member_requested = return_book_form().member_name.data
    book_requested = return_book_form().book_name.data
    paid = return_book_form().paid.data

    if return_book_form().validate_on_submit():
        borrowed_book = Transaction.query.filter(and_(Transaction.type_of_transaction == "borrow" ,
                                                      Transaction.returned == False,
                                                      Transaction.book_name == book_requested,
                                                      Transaction.member == member_requested)).first()
        book = Book.query.filter_by(title = book_requested).first()
        member = Member.query.filter_by(member_name = member_requested).first()
        member.amount = member.amount + paid
        book.borrow_stock = book.borrow_stock + 1
        borrowed_book.returned = True
        return_book = Transaction(book = book.id,
                                  book_name = book.title,
                                  member = member.member_name,
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