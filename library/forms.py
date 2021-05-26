from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError
from library.models import Member, Book, Transaction


# form for creating and updating members
class member_form(FlaskForm):

    # check if unique memberName already exists
    def validate_member_name(self, member_name_to_check):
        member = Member.query.filter_by(member_name=member_name_to_check.data).first()
        if member:
            raise ValidationError('Username already exists! Please try a different Member Name')
    
    # check if phone number already exists
    def validate_phone_number(self, phone_number_to_check):
        phone = Member.query.filter_by(phone_number=phone_number_to_check.data).first()
        if phone: 
            raise ValidationError('Phone Number already exists! Please try a different Phone Number')
   
    name = StringField(label='Name', validators=[Length(min=2, max=30), DataRequired()])
    member_name = StringField(label='Member Name',  validators=[Length(min=2, max=30), DataRequired()])
    phone_number = StringField(label='Phone Number', validators=[DataRequired()])
    submit = SubmitField(label='Submit')



# form for creating and updating books
class book_form(FlaskForm):
    # checks if book already exists
    def validate_title(self, title_to_check):
        book = Book.query.filter_by(title=title_to_check.data).first()
        if book:
            raise ValidationError('Book already exists')

    title = StringField(label='Title', validators=[ DataRequired()])
    isbn = StringField(label='ISBN', validators=[DataRequired()])
    author = StringField(label='Author', validators=[ DataRequired()])
    stock = IntegerField(label='Stock', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


