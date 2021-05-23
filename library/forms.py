from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError
from library.models import Member, Book
from library import db


class member_form(FlaskForm):

    # check if unique memberName already exists
    def validate_member_name(self, member_name_to_check):
        member = Member.query.filter_by(
            member_name=member_name_to_check.data).first()
        if member:  # if member already exists
            raise ValidationError(
                'Username already exists! Please try a different Member Name')

    # check if phone number already exists
    def validate_phone_number(self, phone_number_to_check):
        phone = Member.query.filter_by(
            phone_number=phone_number_to_check.data).first()
        if phone:  # if phone number exists
            raise ValidationError(
                'Phone Number already exists! Please try a different Phone Number')

    name = StringField(label='Name',  validators=[
                       Length(min=2, max=30), DataRequired()])
    member_name = StringField(label='Member Name',  validators=[
                              Length(min=2, max=30), DataRequired()])
    phone_number = IntegerField(
        label='Phone Number', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class book_form(FlaskForm):

    def validate(self):
        book_list = db.session.query(Book.title).all()
        book_list = list(map(' '.join, book_list))
        author_list = db.session.query(Book.author).all()
        author_list = list(map(' '.join, author_list))
        if not super(book_form, self).validate():
                return False

        if self.title.data in book_list and self.author.data in author_list:
            msg = 'Book already exists'
            self.title.errors.append(msg)
            self.author.errors.append(msg)
            return False

    title = StringField(label='Title', validators=[Length(min=2, max=50), DataRequired()])
    isbn = StringField(label='ISBN', validators=[DataRequired()])
    author = StringField(label='Author', validators=[Length(min=2, max=50), DataRequired()])
    stock = IntegerField(label='Stock', validators=[DataRequired()])
    submit = SubmitField(label='Submit')





class search_form(FlaskForm):
    query = StringField(label='')


class delete_form(FlaskForm):
    delete = SubmitField(label="delete")


class borrow_book_form(FlaskForm):
    member_name = StringField(label="Member Name", validators=[DataRequired()])
    book_name = StringField(label="Book Name", validators=[DataRequired()])
    borrow = SubmitField(label="Borrow")
class return_book_form(FlaskForm):
    member_name = StringField(label="Member Name", validators=[DataRequired()])
    book_name = StringField(label="Book Name", validators=[DataRequired()])
    paid = IntegerField(label="Paid", validators=[DataRequired()
    ])
