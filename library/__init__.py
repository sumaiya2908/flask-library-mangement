# External modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '2f82262027aa46e09328b96c' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fcnxppipqwfwxz:cb775483628b0031ad9a448dd1ab159a580408c7a7fa63cca0f395e4b4ac9c97@ec2-34-202-54-225.compute-1.amazonaws.com:5432/d4he96qecvdttk'
db = SQLAlchemy(app)


from library import routes