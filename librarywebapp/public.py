

from flask import request, redirect, flash
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


def search(searched, type):
    form = SearchBookForm()
    form.searched.data = searched
    types = {1: "Title", 2: "Author", 0:"All"}
    if type in types.keys():
        form.searchedType = type
        searched_list = search_func(searched, type)
        return render_template("search.html", form=form, booklist=searched_list, searched = searched)
    else:
        flash("the type is not a valid choice!")
        
        return listbooks()
        
        
    # if form.validate_on_submit():
    #     searched = form.searched.data
    #     searchedType = types[form.searchedType.data]
    #     searched_list = search_func(searched, searchedType)

    


def bookcopies(book_id):
    bookcopies, booktitle =  bookcopies_func(book_id)

    return render_template("bookcopies.html", 
    bookcopies = bookcopies, 
    book_title=booktitle,
    loan_period=timedelta(days = 28),
    overdue_period=timedelta(days = 35),
    today=todaydate)
