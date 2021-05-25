from library import db


class Member(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    member_name = db.Column(db.String(), nullable=False, unique=True)
    phone_number = db.Column(db.String(), nullable=False, unique = True)
    to_pay = db.Column(db.Integer(), default=0)
    total_paid = db.Column(db.Integer(), default = 0)
    borrowed = db.relationship('Book', secondary = 'transaction', backref= 'borrower', lazy='dynamic')



class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    isbn = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    stock = db.Column(db.Integer(), default=0)
    borrow_stock = db.Column(db.Integer(), default=0)
    member_count = db.Column(db.Integer(), default = 0)
    returned = db.Column(db.Boolean(), default = False)

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer(), primary_key=True)
    member = db.Column(db.Integer(), db.ForeignKey('member.id'), nullable = True)
    book = db.Column(db.Integer(), db.ForeignKey('book.id'), nullable = True)
    book_name = db.Column(db.String())
    member_name = db.Column(db.String())
    type_of_transaction = db.Column(db.String(length=7), nullable=False)
    date = db.Column(db.Date())
    amount = db.Column(db.Integer())

