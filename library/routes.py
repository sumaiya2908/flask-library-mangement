from library.forms import BookForm, DeleteForm, MemberForm
from flask import render_template, redirect, url_for, flash, request
from library import app, db
# from library.models import Member, Book
import requests
import json

@app.route('/')
@app.route('/home')
def home_page():
    form_b = BookForm()
    form_m = MemberForm()
    return render_template('home.html', form_b = form_b, form_m = form_m)


