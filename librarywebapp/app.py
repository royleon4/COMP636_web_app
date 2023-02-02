from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import FieldType
import connect

from webforms import SearchForm

app = Flask(__name__)

dbconn = None
connection = None

todaydate = datetime.now().date()

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/listbooks")
def listbooks():
    connection = getCursor()
    connection.execute("SELECT * FROM books;")
    bookList = connection.fetchall()
    print(bookList)
    return render_template("booklist.html", booklist = bookList)    

@app.route("/loanbook")
def loanbook():
    
    connection = getCursor()
    connection.execute("SELECT * FROM borrowers;")
    borrowerList = connection.fetchall()
    sql = """SELECT * FROM bookcopies
inner join books on books.bookid = bookcopies.bookid
 WHERE bookcopyid not in (SELECT bookcopyid from loans where returned <> 1);"""
    connection.execute(sql)
    bookList = connection.fetchall()
    return render_template("addloan.html", loandate = todaydate,borrowers = borrowerList, books= bookList)

@app.route("/loan/add", methods=["POST"])
def addloan():
    borrowerid = request.form.get('borrower')
    bookid = request.form.get('book')
    loandate = request.form.get('book_loan_date')
    print(todaydate)
    cur = getCursor()
    cur.execute("INSERT INTO loans (borrowerid, bookcopyid, loandate, returned) VALUES(%s,%s,%s,0);",(borrowerid, bookid, str(todaydate),))
    return redirect("/currentloans")

@app.route("/listborrowers")
def listborrowers():
    connection = getCursor()
    connection.execute("SELECT * FROM borrowers;")
    borrowerList = connection.fetchall()
    return render_template("borrowerlist.html", borrowerlist = borrowerList)

@app.route("/currentloans")
def currentloans():
    connection = getCursor()
    sql=""" select br.borrowerid, br.firstname, br.familyname,  
                l.borrowerid, l.bookcopyid, l.loandate, l.returned, b.bookid, b.booktitle, b.author, 
                b.category, b.yearofpublication, bc.format 
            from books b
                inner join bookcopies bc on b.bookid = bc.bookid
                    inner join loans l on bc.bookcopyid = l.bookcopyid
                        inner join borrowers br on l.borrowerid = br.borrowerid
            order by br.familyname, br.firstname, l.loandate;"""
    connection.execute(sql)
    loanList = connection.fetchall()
    return render_template("currentloans.html", loanlist = loanList)

# Secret Key!
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

# Pass stuff to Nav Bar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

# Create a search function
@app.route("/search", methods=["POST"])
def search():

    form = SearchForm()
    if form.validate_on_submit():
        searched = form.searched.data
        connection = getCursor()
        sql = """SELECT * FROM books WHERE booktitle LIKE '%{}%' OR author LIKE '%{}%'""".format(searched, searched)
        connection.execute(sql)
        searched_list = connection.fetchall()
        


        return render_template("search.html", form=form, results=searched_list, searched = searched)

@app.route("/bookcopies/<int:book_id>")
def bookcopies(book_id):
    connection = getCursor()
    sql=""" select  
                bc.bookcopyid, bc.format, l.returned, max(l.loandate)
            from bookcopies bc
                inner join books b on bc.bookid = b.bookid
                    left join loans l on bc.bookcopyid = l.bookcopyid
            where b.bookid = {}
            group by l.bookcopyid
            order by l.loandate;""".format(book_id)
    connection.execute(sql)
    bookcopies = connection.fetchall()
    connection.execute("select booktitle, author from books where bookid = {}".format(book_id))
    book_title = connection.fetchall()
    return render_template("bookcopies.html", 
    bookcopies = bookcopies, 
    book_title=book_title,
    loan_period=timedelta(days = 28),
    overdue_period=timedelta(days = 35),
    today=todaydate)


@app.route("/staff")
def staff():
    render_template("staff.html")

