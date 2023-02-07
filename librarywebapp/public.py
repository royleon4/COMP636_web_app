

from flask import request, redirect
from datetime import datetime, timedelta

from features import *

from flask import render_template

from webforms import SearchBookForm


todaydate = datetime.now().date()

def home():
    # print(request.url_rule, request.endpoint)
    form=SearchBookForm()
    return render_template("base.html", form=form)



def listbooks():
    
    booklist = listbooks_func()   
    return render_template("booklist.html", booklist = booklist)


def search():
    form = SearchBookForm()
    types = {"Title":1, "Author":2, "All":0}
    if form.validate_on_submit():
        searched = form.searched.data
        searchedType = types[form.searchedType.data]
        searched_list = search_func(searched, searchedType)

    return render_template("search.html", form=form, booklist=searched_list, searched = searched)


def bookcopies(book_id):
    bookcopies, booktitle =  bookcopies_func(book_id)

    return render_template("bookcopies.html", 
    bookcopies = bookcopies, 
    book_title=booktitle,
    loan_period=timedelta(days = 28),
    overdue_period=timedelta(days = 35),
    today=todaydate)
