# internal imports
from library.forms import book_form, member_form, return_book_form, borrow_book_form
from library import app, db

# external imports 
import requests
import json

from datetime import date
from library.forms import book_form, return_book_form, borrow_book_form
from flask import render_template, redirect, url_for, flash, request, jsonify
from library.models import Book, Member, Transaction
from sqlalchemy import and_, or_, desc


# Renders Home Page
@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home_page():
    books_to_borrow = Book.query.filter(Book.borrow_stock > 0).all()
    members_can_borrows = Member.query.filter(Member.to_pay < 500).all()
    books_to_return =  Book.query.filter(Book.borrower).all()
    return render_template('home.html', member_form = member_form(), book_form = book_form(), books_to_borrow = books_to_borrow, members_can_borrow = members_can_borrows, books_to_return = books_to_return, book = False)



@app.route('/reports', methods = ['GET','POST']) 
def report_page():
    books = Book.query.all()
    members = Book.query.all()
    popular_books_title = []
    books_count = []
    popular_books = Book.query.order_by(desc(Book.member_count)).limit(10).all()
    for book in popular_books:
        popular_books_title.append(book.title)
        books_count.append(book.member_count)
    popular_books_title = json.dumps(popular_books_title)
    books_count = json.dumps(books_count)
    data = json.dumps( [1.0,2.0,3.0, 0.8, 0.7, 0.4] )
    labels=json.dumps( ["12-31-18", "01-01-19", "01-02-19","12-31-18", "01-01-19", "01-02-19"] )
    return render_template("reports.html", labels = labels, book_title = popular_books_title, data = data, book_count = books_count)











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