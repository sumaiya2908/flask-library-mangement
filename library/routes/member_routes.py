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


# Renders member page
@app.route('/members', methods=['GET', 'POST'])
def members_page():
    # read members from db
    member = Member.query.order_by('id').all() 

    form_member = member_form() 
    books_to_borrow = Book.query.filter(Book.borrow_stock > 0).all()
    members_can_borrows = Member.query.filter(Member.to_pay < 500).all()
    books_to_return =  Book.query.filter(Book.borrower).all()
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
    return render_template('members/members.html', member_form=form_member, members=member, length = len(member), books_to_borrow = books_to_borrow, members_can_borrow = members_can_borrows, books_to_return = books_to_return)


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
    v = request.form.get("abc")
    print(v)

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