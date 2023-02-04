
from flask import request, redirect
from datetime import datetime, timedelta
from features import *
from flask import render_template
from webforms import SearchForm, SearchBorrowersForm, updateBorrowerForm as bf, createBorrowerForm

todaydate = datetime.now().date()
prefix = '/' + 'staff'


def staff():
    return render_template("staff.html")


def staffloanbook():

    borrowerList, bookList = loanbook_func()

    return render_template("/addloan.html", loandate = todaydate,borrowers = borrowerList, books= bookList)

def addloan():

    borrowerid = request.form.get('borrower')
    bookid = request.form.get('book')
    addloan_func(borrowerid, bookid, todaydate)

    return redirect(f"{prefix}/currentloans")

def stafflistbooks():
    
    booklist = listbooks_func()   
    return render_template("booklist.html", booklist = booklist)

def listborrowers():
    borrowerList = listborrowers_func()
    
    return render_template("borrowerlist.html", borrowerlist = borrowerList)


def staffcurrentloans():
    loanList = currentloans_func()
    return render_template("currentloans.html", 
    loanlist = loanList)

# Create a search function

def staffsearch():
    form = SearchForm()
    if form.validate_on_submit():
        searched = form.searched.data
        searched_list = search_func(searched)

    return render_template("search.html", form=form, results=searched_list, searched = searched)


def staffbookcopies(book_id):
    bookcopies, booktitle =  bookcopies_func(book_id)

    return render_template("bookcopies.html", 
    bookcopies = bookcopies, 
    book_title=booktitle,
    loan_period=timedelta(days = 28),
    overdue_period=timedelta(days = 35),
    today=todaydate)

def searchBorrowers():
    form = SearchBorrowersForm()
    # print(form.searchedBorrowers.data, form.selectedType.data)
    # print(request.form.get('selectedType'))
    
    if form.validate_on_submit():
        searched = form.searchedBorrowers.data
        typeOfSearch = form.selectedType.data
        borrower = searchBorrowers_func(searched, typeOfSearch)
        # print(borrower)
        return render_template("borrowerlist.html", borrowerlist=borrower)

def updateBorrowerForm(borrower_id):

    borrower = searchBorrowers_func(borrower_id, "ID")

    return render_template(
        "updateborrower.html", 
        borrower=borrower)

def updateBorrower(borrower_id):

    form = bf()

    if form.validate_on_submit():
        ftn=form.firstname.data
        fyn=form.familyname.data
        dob=request.form.get('dob')
        house=form.housenumber.data
        street=form.street.data
        city=form.city.data
        town=form.town.data
        poco=form.postcode.data

        code = updateBorrower_func(borrower_id, ftn, fyn, dob, 
        house, street, town, city, poco)
    print(f'CODE: {code}')
    
    return redirect(f"{prefix}/listborrowers")

def newBorrower():
    return render_template("addborrower.html")
    


def createBorrower():

    form = createBorrowerForm()

    if form.validate_on_submit():
        ftn=form.firstname.data
        fyn=form.familyname.data
        dob=request.form.get('dob')
        house=form.housenumber.data
        street=form.street.data
        city=form.city.data
        town=form.town.data
        poco=form.postcode.data

        code = createBorrower_func(ftn, fyn, dob, 
        house, street, town, city, poco)
    print(f'CODE: {code}')
    
    return redirect(f"{prefix}/listborrowers")

def loanreturn(bookid, borrowerid):

    loanreturn_func(bookid, borrowerid)

    return redirect(f"{prefix}/currentloans")

def overdueloans():
    loanList = currentloans_func()
    return render_template("overdueloans.html", 
    loanlist=loanList, todaydate=todaydate, 
    loan_period=timedelta(days = 28),
    overdue_period=timedelta(days = 35))
    
    
    