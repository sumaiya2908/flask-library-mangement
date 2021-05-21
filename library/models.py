from library import db
from sqlalchemy.orm import relationship

class Member(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    member_name = db.Column(db.String(length=30), nullable=False, unique=True)
    phone_number = db.Column(db.Integer())
    feePaid = db.Column(db.Integer())
    feeDebt = db.Column(db.Integer())

class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=50), nullable=False)
    isbn = db.Column(db.String(length=15), nullable=False)
    author = db.Column(db.Integer(), nullable=False)
    stock = db.Column(db.Integer(), default=0, nullable=False)

