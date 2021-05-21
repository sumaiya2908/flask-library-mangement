from library.forms import BookForm, DeleteForm, MemberForm
from flask import render_template, redirect, url_for, flash, request
from library import app, db
from library.models import Member, Book
import requests
import json

@app.route('/')
@app.route('/home')
def home_page():
    form_b = BookForm()
    form_m = MemberForm()
    return render_template('home.html', form_b = form_b, form_m = form_m)


@app.route('/books', methods=['GET', 'POST'])
def books_page():
    formB = BookForm()
    books = Book.query.all()  #books to read
    if formB.validate_on_submit(): #if no error 
        book_to_create = Book(title=formB.title.data,  #add book to db
                              isbn=formB.isbn.data,
                              author=formB.author.data,
                              stock=formB.stock.data)
        db.session.add(book_to_create)
        db.session.commit()
        return redirect(url_for('books_page'))
    if formB.errors != {}:  # If there are not errors from the validations
        for err_msg in formB.errors.values():
            flash(
                f'There was an error with creating a book: {err_msg}', category='danger')
    return render_template('books.html', formB=formB, books=books)


@app.route('/members', methods=['GET', 'POST'])
def members_page():
    formM = MemberForm()
    member = Member.query.all() #members to read
    if formM.validate_on_submit():
        member_to_create = Member(name=formM.name.data,     #add member to db
                                  phone_number=formM.phone_number.data,
                                  member_name=formM.member_name.data)
        db.session.add(member_to_create)
        db.session.commit()
        return redirect(url_for('members_page'))
    if formM.errors != {}:  # If there are not errors from the validations
        for err_msg in formM.errors.values():
            flash(
                f'There was an error with creating a Member: {err_msg}', category='danger')
    return render_template('members.html', formM=formM, members=member)


@app.route('/delete-book/<book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('books_page'))


@app.route('/delete-member/<member_id>', methods=['POST'])
def delete_member(member_id):
    member = Member.query.filter_by(id=member_id).first()
    db.session.delete(member)
    db.session.commit()
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