# Overview
## A flask library management system
### [Deployed on heroku](https://flask-library-management.herokuapp.com/)

![home](/screenshots/Screenshot%20(128).png)
## Stacks used

- HTML
- CSS
- JavaScript
- Bootstarp
- Flask(python framework)
- SQLAlchemy(postgreSQL)
- Flask forms 
- ChartJS


## [Installation](#installation)
## Features

- [Create, Upadate , Read and Delete Books and Members](#crud-operations)
- [Import books from Frappe API](#import-books-from-frappe-api)
- [Issue a book to a member](#issue-a-book)
- [Return a book from a member](#return-a-book)
- [Manage Transactions](#transaction-records)
- [Search book or author](#search-books-and-authors)
- [See reports of top 10 popular books and most paying customers](#reports)

***
## Installation
- Run the command to cole the repository
```sh
  git clone https://github.com/sumaiya119/flask-library-mangement.git
```
- Install all requirements with
```sh
cd flask-library-management
pip install -r requirements.txt
```
- Set your secret key in /library/\_\_init\_\_.py file
- for creating a local DB
```sh
python
>>from library import db
>>db.create_all()
```
- run commad to start the server
```sh
flask run
```
***
## CRUD operations

### Read books from Database and dipslayed in the form of table
![book-create](/screenshots/Screenshot%20(129).png)

![create](/screenshots/Screenshot%20(130).png)
***
## Import books from Frappe API

### Import books by title
![import](/screenshots/Screenshot%20(131).png)
***
## Issue a book
### Issue a book to a member using dropdown where book(with stock>0) and members(to_pay<500) are displayed
![borrow](/screenshots/Screenshot%20(132).png)
***
## Return a book
### Retuen a book from members 
![return](/screenshots/Screenshot%20(142).png)
***
## Transaction Records
![transaction](/screenshots/Screenshot%20(134).png)
***
## Search Books and authors
![search](/screenshots/Screenshot%20(136).png)
***
## Reports
### Report of top 10 books
![book](/screenshots/Screenshot%20(137).png)

### Report of top 10 highest paying members
![members](/screenshots/Screenshot%20(138).png)
