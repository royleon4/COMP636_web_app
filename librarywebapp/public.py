from flask import request, redirect
from datetime import datetime, timedelta

from features import *

from flask import render_template



todaydate = datetime.now().date()

def home():

    return render_template("base.html")



def listbooks():
    
    booklist = listbooks_func()   
    return render_template("booklist.html", booklist = booklist)


def search():
    searched = request.form.get("searched")
    types = {"Title":1, "Author":2, "All":0}
    searchedType = types[request.form.get("selectedtype")]


    searched_list = search_func(searched, searchedType)

    return render_template("search.html", booklist=searched_list, searched = searched)


def bookcopies(book_id):
    bookcopies, booktitle =  bookcopies_func(book_id)

    return render_template("bookcopies.html", 
    bookcopies = bookcopies, 
    book_title=booktitle,
    loan_period=timedelta(days = 28),
    overdue_period=timedelta(days = 35),
    today=todaydate)
