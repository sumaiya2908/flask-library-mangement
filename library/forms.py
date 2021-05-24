from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError
from library.models import Member, Book, Transaction
from sqlalchemy import and_

# form for creating and updating members
class member_form(FlaskForm):

    # check if unique memberName already exists
    # def validate_member_name(self, member_name_to_check):
    #     member = Member.query.filter_by(member_name=member_name_to_check.data).first()
    #     if member:
    #         raise ValidationError('Username already exists! Please try a different Member Name')

    
    # check if phone number already exists
    # def validate_phone_number(self, phone_number_to_check):
    #     phone = Member.query.filter_by(phone_number=phone_number_to_check.data).first()
    #     if phone: 
    #         raise ValidationError('Phone Number already exists! Please try a different Phone Number')

   
    name = StringField(label='Name', validators=[Length(min=2, max=30), DataRequired()])
    member_name = StringField(label='Member Name',  validators=[Length(min=2, max=30), DataRequired()])
    phone_number = StringField(label='Phone Number', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


# form for creating and updating books
class book_form(FlaskForm):


    # def validate(self):
    #     book = Book.query.filter_by(title = self.title.data)
    #     author = Book.query.filter_by(author = self.author.data)
    #     if not super(book_form, self).validate():
    #             return False
       
    #     if book and author:
    #         msg = 'Book already exists'
    #         self.title.errors.append(msg)
    #         self.author.errors.append(msg)
    #         return False


    title = StringField(label='Title', validators=[Length(min=2, max=50), DataRequired()])
    isbn = StringField(label='ISBN', validators=[DataRequired()])
    author = StringField(label='Author', validators=[Length(min=2, max=50), DataRequired()])
    stock = IntegerField(label='Stock', validators=[DataRequired()])
    submit = SubmitField(label='Submit')



#form for borrowing books
class borrow_book_form(FlaskForm):

    #validations for borrowing books
    # def validate(self):
    #     book = Book.query.filter_by(title = self.book_name.data).first()
    #     member = Member.query.filter_by(member_name = self.member_name.data).first()
    #     if not super(borrow_book_form, self).validate():
    #             return False
                
    #     if  book is None:
    #         msg = "Book Doesnot Exist"
    #         self.book_name.errors.append(msg)
    #         return False
    #     if book.borrow_stock == 0:
    #         msg = "No stock"
    #         self.book_name.errors.append(msg)
    #         return False
    #     if member is None:
    #         msg = "Member Doesnot Exist"
    #         self.member_name.errors.append(msg)
    #         return False
    #     if member.amount >= 500:
    #         msg = "The customer has overdue rent of 500"
    #         self.member_name.errors.append(msg)
    #         return False
    #     else:
    #         return True


    member_name = StringField(label="Member Name", validators=[DataRequired()])
    book_name = StringField(label="Book Name", validators=[DataRequired()])
    borrow = SubmitField(label="Borrow")


# form for returning a book
class return_book_form(FlaskForm):


    # def validation(self):
    #     book = Book.query.filter_by(title = self.book_name.data).first()
    #     member = Member.query.filter_by(member_name = self.member_name.data).first()

    #     borrowed_book = Transaction.query.filter(and_(Transaction.type_of_transaction == "borrow" ,
    #                                                   Transaction.returned == False,
    #                                                   Transaction.book_name == book,
        
    #                                                   Transaction.member == member)).all()
    #     if not super(return_book_form, self).validate():
    #             return False

    #     if(borrowed_book is None):
    #         msg = "No record of issue"
    #         self.book_name.errors.append(msg)
    #         return False



    member_name = StringField(label="Member Name", validators=[DataRequired()])
    book_name = StringField(label="Book Name", validators=[DataRequired()])
    paid = IntegerField(label="Pay", validators=[DataRequired()])
    submit = SubmitField(label="Return")
