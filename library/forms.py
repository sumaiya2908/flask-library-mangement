from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError
from library.models import Member, Book


class MemberForm(FlaskForm):

    def validate_memberName(self, member_name_to_check): #check if unique memberName already exists
        member = Member.query.filter_by(
            member_name=member_name_to_check.data).first()
        if member: #if member already exists
            raise ValidationError(  #throws error
                'Username already exists! Please try a different Member Name')

    def validate_phoneNumber(self, phone_number_to_check): #check if phone number already exists
        phone = Member.query.filter_by(
            phone_number=phone_number_to_check.data).first()
        if phone: #if phone number exists
            raise ValidationError( #throws error
                'Phone Number already exists! Please try a different Phone Number')

    name = StringField(label='Name',  validators=[
                       Length(min=2, max=30), DataRequired()])
    member_name = StringField(label='Member Name',  validators=[
                             Length(min=2, max=30), DataRequired()])
    phone_number = IntegerField(label='Phone Number',
                               validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class BookForm(FlaskForm):

    # def validate_title(self, title_to_check): #check if book name already exists
    #     book = Book.query.filter_by(title=title_to_check.data).first()
    #     if book:
    #         raise ValidationError('Book already Exists!')


    title = StringField(label='Title',  validators=[
                        Length(min=2, max=50), DataRequired()])
    isbn = StringField(label='ISBN',  validators=[DataRequired()])
    author = StringField(label='Author', validators=[
                         Length(min=2, max=50), DataRequired()])
    stock = IntegerField(label='Stock', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class SearchForm(FlaskForm):
    query = StringField(label='')


class DeleteForm(FlaskForm):
    delete = SubmitField(label="delete")
