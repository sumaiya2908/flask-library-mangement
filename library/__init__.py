# External modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# ENV = 'dev'

# if(ENV == 'dev'):
    # app.config['SQLALCHEMY_DATABASE_URI'] = 
# else:
# app = Flask(__name__)
app.config['SECRET_KEY'] = '2f82262027aa46e09328b96c' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from library.routes import routes, book_routes, member_routes, transaction_routes 