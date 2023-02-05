# This file contains reusable functions shared by staff and public
# This is the only file deals with database

import re
import mysql.connector
import connect


def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

def listbooks_func():
    connection = getCursor()


    # sql_books = "SELECT * FROM books;"

    # sql_loansum = """SELECT *, ls.loantimes FROM books b 
    #             inner join 
    #                 (Select title, bookid as ID, sum(Times) as loantimes from (select b.booktitle as title, b.bookid as bookid, count(bc.bookcopyid) as Times 
    #                 FROM bookcopies bc 
    #                 left join loans l on bc.bookcopyid=l.bookcopyid
    #                 inner join books b on bc.bookid=b.bookid
    #                 group by bc.bookcopyid) as cpt 
    #                 group by bookid 
    #                 order by bookid) as ls
    #             WHERE ls.ID=b.bookid;
                    
    #                 """
                
    connection.execute("SELECT * FROM books;")
    bookList = connection.fetchall()
    return bookList 


def loanbook_func():
    
    connection = getCursor()
    connection.execute("SELECT * FROM borrowers;")
    borrowerList = connection.fetchall()
    sql = """SELECT * FROM bookcopies bc
inner join books b on b.bookid = bc.bookid
 WHERE bookcopyid not in (SELECT bookcopyid from loans where returned <> 1) OR bc.format in ('ebook', 'Audio Book');"""
    connection.execute(sql)
    bookList = connection.fetchall()
    return borrowerList, bookList

def addloan_func(borrowerid, bookid, datetime):

    cur = getCursor()
    cur.execute("INSERT INTO loans (borrowerid, bookcopyid, loandate, returned) VALUES(%s,%s,%s,0);",(borrowerid, bookid, str(datetime),))
    return 

def listborrowers_func():
    connection = getCursor()
    connection.execute("SELECT * FROM borrowers;")
    borrowerList = connection.fetchall()
    return borrowerList

def currentloans_func():
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
    return loanList
    

def search_func(searched):

    connection = getCursor()
    sql = """SELECT * FROM books WHERE booktitle LIKE '%{}%' OR author LIKE '%{}%'""".format(searched, searched)
    connection.execute(sql)
    searched_list = connection.fetchall()
    return searched_list

def bookcopies_func(book_id):
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
    booktitle = connection.fetchall()
    return bookcopies, booktitle

def searchBorrowers_func(searched, type):
    connection = getCursor()
    sql =""
    if type == "Name": 
        sql=""" SELECT * FROM borrowers WHERE firstname LIKE '%{}%' OR familyname LIKE '%{}%' """.format(searched, searched)
    if type == "ID":
        sql=""" SELECT * FROM borrowers WHERE borrowerid = {} """.format(searched)
    
    connection.execute(sql)
    borrowers = connection.fetchall()

    return borrowers
def updateBorrower_func(
    id, firstname=None, lastname=None, DoB=None, house=None, street=None, town=None, city=None, postcode=None):

    update_list = { 
        "firstname":firstname, "familyname":lastname, 
        "dateofbirth":DoB, "housenumbername":house, 
        "street":street, "town":town, 
        "city": city, "postalcode": postcode }

    if all(item is None or item == "" for item in update_list.values()):
        return 500
    sql = """UPDATE borrowers SET """

    for field, key in update_list.items():
        if key != "" and key is not None:
            sql += f"{field} = '{key}', "

    sql = sql.strip(', ')
    sql += f" WHERE borrowerid = {id}"

    connection = getCursor()

    connection.execute(sql)
    borrowers = connection.fetchall()

    return 200


def createBorrower_func(
    firstname=None, lastname=None, 
    DoB=None, house=None, street=None, 
    town=None, city=None, postcode=None):

    update_list = { 
        "firstname":firstname, "familyname":lastname, 
        "dateofbirth":DoB, "housenumbername":house, 
        "street":street, "town":town, 
        "city": city, "postalcode": postcode }

    sql = "INSERT INTO borrowers ("
    values = " VALUES ( "

    print(update_list)

    for field, key in update_list.items():
        print(sql + values)
        if key == "" or key is None:
            return 500
        sql += f"{field}, "
        values += f"'{key}', "

    sql, values = sql.strip(', '), values.strip(', ')

    sql += ") "
    values += ")" 

    # print(sql + values)

    connection = getCursor()

    connection.execute(sql+values)

    return 200

def loanreturn_func(bookcopy_id, borrower_id):

    sql = f"UPDATE loans SET returned = 1 WHERE bookcopyid={bookcopy_id} AND borrowerid={borrower_id};"

    print(sql)
    connection = getCursor()

    connection.execute(sql)
    
    return 200

def loansummary_func():
    sql = """Select title, bookid as ID, sum(Times) as loantimes from (select b.booktitle as title, b.bookid as bookid, count(bc.bookcopyid) as Times 
				FROM bookcopies bc 
				left join loans l on bc.bookcopyid=l.bookcopyid
				inner join books b on bc.bookid=b.bookid
				group by bc.bookcopyid) as cpt 
                group by bookid 
                order by bookid;"""

    connection = getCursor()
    connection.execute(sql)
    table = connection.fetchall()

    return table


def borrowersummary_func():
    sql = """SELECT br.borrowerid as ID, br.firstname, br.familyname, count(l.borrowerid) as loans 
                FROM borrowers br 
                left join loans l on br.borrowerid=l.borrowerid 
                group by br.borrowerid;"""

    connection = getCursor()
    connection.execute(sql)
    table = connection.fetchall()

    return table