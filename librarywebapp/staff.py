from flask import request, redirect, flash
from datetime import datetime, timedelta
from features import *
from flask import render_template

todaydate = datetime.now().date()
prefix = '/' + 'staff'


def staff():
    
    return render_template("staff.html")


def staffloanbook():


    borrowerlist, booklist = loanbook_func()

    return render_template("/addloan.html", booklist=booklist, borrowerlist=borrowerlist, loandate = todaydate)

def addloan():

    borrowerid = request.form.get("selectborrower")
    bookid = request.form.get("selectbook")
    loandate = request.form.get("loandate")


    return redirect(f"{prefix}/currentloans")

    

    
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

    
    return render_template("borrowerlist.html", borrowerlist = borrowerList)


def staffcurrentloans():
    loanList = currentloans_func()
    return render_template("currentloans.html", 
    loanlist = loanList)

# Create a search function

def staffsearch():

    searched = request.form.get("searched")
    types = {"Title":1, "Author":2, "All":0}
    searchedType = types[request.form.get("selectedtype")]


    searched_list = search_func(searched, searchedType)

    return render_template("search.html", booklist=searched_list, searched = searched)


def staffbookcopies(book_id):
    bookcopies, booktitle =  bookcopies_func(book_id)

    return render_template("bookcopies.html", 
    bookcopies = bookcopies, 
    book_title=booktitle,
    loan_period=timedelta(days = 28),
    overdue_period=timedelta(days = 35),
    today=todaydate)

def searchBorrowers():


    searched = request.form.get("searchedborrower")
    typeofsearched = request.form.get("searchedtype")

    

    if typeofsearched == "ID" and not searched.isdigit():
        flash('Enter digits when searching for ID, please!')
        return render_template("borrowerlist.html")
        
    borrower = searchBorrowers_func(searched, typeofsearched)
        
    return render_template("borrowerlist.html", borrowerlist=borrower)


def updateBorrowerForm(borrower_id):

    borrower = searchBorrowers_func(borrower_id, "ID")

    return render_template(
        "updateborrower.html", 
        borrower=borrower)

def updateBorrower(borrower_id):


    ftn = request.form.get("fname")
    fyn = request.form.get("lname")
    dob = request.form.get("dob")
    house = request.form.get("house")
    street = request.form.get("street")
    town = request.form.get("town")
    city = request.form.get("city")
    poco = request.form.get("pcode")


    code = updateBorrower_func(borrower_id, ftn, fyn, dob, 
        house, street, town, city, poco)
    print(f'CODE: {code}')

    
    return redirect(f"{prefix}/listborrowers")

def newBorrower():

    return render_template("addborrower.html")
    


def createBorrower():


    ftn = request.form.get("fname")
    fyn = request.form.get("lname")
    dob = request.form.get("dob")
    house = request.form.get("house")
    street = request.form.get("street")
    town = request.form.get("town")
    city = request.form.get("city")
    poco = request.form.get("pcode")

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
    

def loansummary():
    table = loansummary_func()

    return render_template("loansummary.html", summary=table)

def borrowersummary():
    table = borrowersummary_func()

    return render_template("borrowersummary.html", summary=table)
    