# internal imports
from library import app, db

# external imports 
import requests

from datetime import date
from flask import render_template, redirect, url_for, flash, request
from library.models import Book, Member, Transaction, Book_borrowed


# Renders transaction page
@app.route('/transactions')
def transactions_page():
    # reads all transactions
    transaction = Transaction.query.order_by('id').all()
    books_to_borrow = Book.query.filter(Book.borrow_stock > 0).all()
    members_can_borrows = Member.query.filter(Member.to_pay < 500).all()
    books_to_return =  Book.query.filter(Book.borrower).all()
    return render_template('transactions/transactions.html', 
                            transactions = transaction, length=len(transaction), 
                            books_to_borrow = books_to_borrow, 
                            members_can_borrow = members_can_borrows, 
                            books_to_return = books_to_return)


@app.route('/borrow-book', methods=['GET','POST'])
def borrow_book():
    # reads the form values
    member_requested = request.form.get("member_name")
    book_requested = request.form.get("book_name")
    member = Member.query.get(int(member_requested))
    book = Book.query.get(int(book_requested))

    if(book and member):
        member.to_pay = member.to_pay + 30
        book.borrow_stock = book.borrow_stock - 1
        book.member_count = book.member_count + 1
        borrow = Book_borrowed(book = book.id,
                               member = member.id)
        borrow_book = Transaction(book_name = book.title,
                                  member_name = member.member_name,
                                  type_of_transaction = "borrow",
                                  amount = 0,
                                  date= date.today())
        db.session.add(borrow_book)
        db.session.add(borrow)
        db.session.commit()
        flash(f"Issued book", category='success')

    else:
        flash(f'Enter the Value', category = 'danger')

    return redirect(request.referrer)


@app.route('/return-book', methods=['GET','POST'])
def return_book():
    # reads form values
    member_requested = request.form.get("member_name")
    book_requested = request.form.get("book_name")
    Ispaid = request.form.get("paid")
    paid = 0
    member = Member.query.get(member_requested)
    book = Book.query.get(book_requested)

    if(Ispaid == 'on'):
        paid = 30

    if(member and book):
        member.to_pay = member.to_pay - paid
        member.total_paid = member.total_paid + paid
        book.borrow_stock = book.borrow_stock + 1
        book.borrower.remove(member)
        return_book = Transaction(book_name = book.title,
                                  member_name = member.member_name,
                                  type_of_transaction = "return",
                                  amount = paid,
                                  date= date.today())
        db.session.add(return_book)
        db.session.commit()
        flash(f"Returned book from {member_requested}", category='success')
    
    else:
        flash(f'error in returning the book', category = 'danger')

    return redirect(request.referrer)