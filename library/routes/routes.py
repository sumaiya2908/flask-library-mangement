# internal imports
from library.forms import book_form, member_form
from library import app, db

# external imports 
import requests
import json

from datetime import date
from flask import render_template, redirect, url_for, flash, request
from library.models import Book, Member
from sqlalchemy import desc


# Renders Home Page
@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home_page():
    #checks the eligibility for borrowing books
    books_to_borrow = Book.query.filter(Book.borrow_stock > 0).all()
    members_can_borrows = Member.query.filter(Member.to_pay < 500).all()
    #reads the book to be borrowed
    books_to_return =  Book.query.filter(Book.borrower).all()
    return render_template('home.html', member_form = member_form(),
                            book_form = book_form(), 
                            books_to_borrow = books_to_borrow, 
                            members_can_borrow = members_can_borrows, 
                            books_to_return = books_to_return, book = False)


@app.route('/reports', methods = ['GET','POST']) 
def report_page():
    books = Book.query.all()
    members = Member.query.all()
    
    popular_books_title = []
    books_count = []
    member_paying_most = []
    member_paid = []
    # reads top 10 books in descending order
    popular_books = Book.query.order_by(desc(Book.member_count)).limit(10).all()
    # reads top highest paying customers
    most_paying_members = Member.query.order_by(desc(Member.total_paid)).limit(10).all()
    for book in popular_books:
        if book.member_count > 0:
            popular_books_title.append(book.title[0:20])
            books_count.append(book.member_count)

    popular_books_title = json.dumps(popular_books_title)
    books_count = json.dumps(books_count)

    for member in most_paying_members:
        if member.total_paid > 0:
            member_paying_most.append(member.member_name)
            member_paid.append(member.total_paid)

    member_paying_most = json.dumps((member_paying_most))
    member_paid = json.dumps((member_paid))

    return render_template("reports.html",members = len(members), 
                            books = len(books), member_paid = member_paid, 
                            book_title = popular_books_title, 
                            members_name = member_paying_most, 
                            book_count = books_count)

