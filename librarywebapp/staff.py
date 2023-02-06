from flask import request, redirect, flash
from datetime import datetime, timedelta
from features import *
from flask import render_template
from webforms import SearchBookForm, SearchBorrowersForm, UpdateBorrowerForm as bf, CreateBorrowerForm, AddLoanForm

todaydate = datetime.now().date()
prefix = '/' + 'staff'


def staff():
    form=SearchBookForm()
    return render_template("staff.html", form=form)


def staffloanbook():

    form = AddLoanForm()
    borrowerList, bookList = loanbook_func()

    for borrower in borrowerList:
        b_id = borrower[0]
        name = f"{borrower[1]} {borrower[2]}"
        form.borrower.choices.append((b_id, name))
    
    for book in bookList:
        b_id = book[0]
        title = f"{b_id}: {book[4]} / {book[2]}"
        form.book.choices.append((b_id, title))

    return render_template("/addloan.html", form=form, loandate = todaydate)

def addloan():

    form = AddLoanForm()

    if form.validate_on_submit():
        borrowerid = form.borrower.data
        bookid = form.book.data
        addloan_func(borrowerid, bookid, todaydate)
        return redirect(f"{prefix}/currentloans")

    for err, decr in form.errors.items():
        print(err, decr)

    return
    

    
def stafflistbooks():
    
    booklist = listbooks_func()   
    loansummary = loansummary_func()
    new_list = []

    counter = 0
    for book in booklist:
        book = list(book)
        book.append(int(loansummary[counter][2]))
        counter+=1
        print(book)
        new_list.append(tuple(book))

        
    return render_template("booklist.html", booklist = new_list)

def listborrowers():
    borrowerList = listborrowers_func()
    form = SearchBorrowersForm()
    
    return render_template("borrowerlist.html", borrowerlist = borrowerList, form=form)


def staffcurrentloans():
    loanList = currentloans_func()
    return render_template("currentloans.html", 
    loanlist = loanList)

# Create a search function

def staffsearch():
    form = SearchBookForm()
    types = {"Title":1, "Author":2, "All":0}
    if form.validate_on_submit():
        searched = form.searched.data
        searchedType = types[form.searchedType.data]
        searched_list = search_func(searched, searchedType)

    return render_template("search.html", form=form, booklist=searched_list, searched = searched)


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

    searched = form.searchedBorrowers.data
    typeOfSearch = form.selectedTypeRadio.data

    if typeOfSearch == "ID" and not searched.isdigit():
        flash('Enter digits when searching for ID, please!')
        return render_template("borrowerlist.html", form=form)
        


    if form.validate_on_submit():
        searched = form.searchedBorrowers.data
        typeOfSearch = form.selectedTypeRadio.data
        borrower = searchBorrowers_func(searched, typeOfSearch)
        
        return render_template("borrowerlist.html", borrowerlist=borrower, form=form)
    return render_template("borrowerlist.html", form=form)

def updateBorrowerForm(borrower_id):

    borrower = searchBorrowers_func(borrower_id, "ID")
    form = bf()

    form.dateofbirth.default = borrower[0][3]

    print(form.dateofbirth.default)

    return render_template(
        "updateborrower.html", 
        borrower=borrower, form=form)

def updateBorrower(borrower_id):

    form = bf()

    if form.validate_on_submit():
        ftn=form.firstname.data
        fyn=form.familyname.data
        dob=form.dateofbirth.data
        house=form.housenumber.data
        street=form.street.data
        city=form.city.data
        town=form.town.data
        poco=form.postcode.data

        code = updateBorrower_func(borrower_id, ftn, fyn, dob, 
        house, street, town, city, poco)
        print(f'CODE: {code}')

    print(form.errors)
    print(form.dateofbirth.data)
    
    return redirect(f"{prefix}/listborrowers")

def newBorrower():
    form = CreateBorrowerForm()

    return render_template("addborrower.html", form=form)
    


def createBorrower():

    form = CreateBorrowerForm()

    if form.validate_on_submit():
        ftn=form.firstname.data
        fyn=form.familyname.data
        dob=form.dateofbirth.data
        house=form.housenumber.data
        street=form.street.data
        city=form.city.data
        town=form.town.data
        poco=form.postcode.data

        code = createBorrower_func(ftn, fyn, dob, 
        house, street, town, city, poco)
        print(f'CODE: {code}')
        
    flash(form.errors)
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
    

def loansummary():
    table = loansummary_func()

    # print(table)

    return render_template("loansummary.html", summary=table)

def borrowersummary():
    table = borrowersummary_func()

    return render_template("borrowersummary.html", summary=table)
    