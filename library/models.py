from library import db
from json import JSONEncoder
class Member(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    member_name = db.Column(db.String(), nullable=False, unique=True)
    phone_number = db.Column(db.BigInteger())
    to_pay = db.Column(db.Integer(), default=0)
    transactions = db.relationship('Transaction', backref='borrowed_member', lazy=True)


    

class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    isbn = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    stock = db.Column(db.Integer(), default=0)
    borrow_stock = db.Column(db.Integer(), default=0)
    member = db.Column(db.Integer(), default = 0) 
    transactions = db.relationship('Transaction', backref='borrowed_book', lazy=True)


class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    book = db.Column(db.Integer(), db.ForeignKey('book.id'))
    book_name = db.Column(db.String())
    member = db.Column(db.Integer(), db.ForeignKey('member.id'))
    type_of_transaction = db.Column(db.String(length=7), nullable=False)
    date = db.Column(db.Date())
    returned = db.Column(db.Boolean(), default = False)
    amount = db.Column(db.Integer())

