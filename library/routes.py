import requests
import json

from library.forms import BookForm, DeleteForm, MemberForm
from flask import render_template, redirect, url_for, flash, request
from library import app, db
from library.models import Member, Book


# Renders Home Page
@app.route('/')
@app.route('/home')
def home_page():
    # Forms from flask forms
    book_form = BookForm()
    member_form = MemberForm()
    return render_template('home.html', book_form = book_form, member_form = member_form)


# Renders Books Page
@app.route('/books', methods=['GET', 'POST'])
def books_page():
    book_form = BookForm()
    delete_form = DeleteForm()
    books = Book.query.all()  # Read books from db
    if book_form.validate_on_submit():  # if no error
        # Create a book in db
        book_to_create = Book(title = book_form.title.data,
                              isbn = book_form.isbn.data,
                              author = book_form.author.data,
                              stock = book_form.stock.data)
        db.session.add(book_to_create)
        db.session.commit()
        return redirect(url_for('books_page'))
    if book_form.errors != {}:  # If there are no errors from the validations
        for err_msg in book_form.errors.values():
            flash(f'There was an error with creating a book: {err_msg}', category='danger')
    return render_template('books/books.html', book_form=book_form, form = delete_form, books=books)


# Renders Members Page
@app.route('/members', methods=['GET', 'POST'])
def members_page():
    member_form = MemberForm()
    member = Member.query.all()  # members to read
    if member_form.validate_on_submit():
        # Create a member in db
        member_to_create = Member(name = member_form.name.data,  # add member to db
                                  phone_number = member_form.phone_number.data,
                                  member_name = member_form.member_name.data)
        db.session.add(member_to_create)
        db.session.commit()
        return redirect(url_for('members_page'))
    if member_form.errors != {}:  # If there are not errors from the validations
        for err_msg in member_form.errors.values():
            flash(f'There was an error with creating a Member: {err_msg}', category = 'danger')
    return render_template('members/members.html', member_form=member_form, members=member)


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
    if len(books) > 0:
        for book in books:
            book_to_create = Book(title=book['title'],  # add book to db
                                  isbn=(book['isbn']),
                                  author=book['authors'],
                                  stock=0)
            db.session.add(book_to_create)
            db.session.commit()
        flash("succesfully Imported", category="success")
    else:
        flash("Not Returned", category="danger")
    return redirect(url_for('books_page'))

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