# External modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY'] 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from library.routes import routes, book_routes, member_routes, transaction_routes 