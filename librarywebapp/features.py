# This file contains reusable functions shared by staff and public
# This is the only file deals with database

import mysql.connector
import connect


def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser,
                                         password=connect.dbpass, host=connect.dbhost,
                                         database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn


def listbooks_func():
    connection = getCursor()

    connection.execute("SELECT * FROM books;")
    bookList = connection.fetchall()
    return bookList


def loanbook_func():

    connection = getCursor()
    connection.execute("SELECT * FROM borrowers;")
    borrowerList = connection.fetchall()
    sql = """SELECT 
                *
            FROM
                bookcopies bc
                    INNER JOIN
                books b ON b.bookid = bc.bookid
            WHERE
                bookcopyid NOT IN (SELECT 
                        bookcopyid
                    FROM
                        loans
                    WHERE
                        returned <> 1)
                    OR bc.format IN ('ebook' , 'Audio Book');"""
    connection.execute(sql)
    bookList = connection.fetchall()

    return borrowerList, bookList


def addloan_func(borrowerid, bookid, datetime):

    cur = getCursor()
    cur.execute("INSERT INTO loans (borrowerid, bookcopyid, loandate, returned) VALUES(%s,%s,%s,0);",
                (borrowerid, bookid, str(datetime),))


def listborrowers_func():
    sql = """SELECT 
                borrowers.borrowerid,
                CONCAT(borrowers.firstname,
                        ' ',
                        borrowers.familyname),
                borrowers.dateofbirth,
                borrowers.housenumbername,
                borrowers.street,
                borrowers.town,
                borrowers.city,
                borrowers.postalcode
            FROM
                borrowers;"""
    connection = getCursor()
    connection.execute(sql)
    borrowerList = connection.fetchall()
    return borrowerList


def currentloans_func():
    connection = getCursor()
    sql = """ SELECT 
                br.borrowerid,
                br.firstname,
                br.familyname,
                l.borrowerid,
                l.bookcopyid,
                l.loandate,
                l.returned,
                b.bookid,
                b.booktitle,
                b.author,
                b.category,
                b.yearofpublication,
                bc.format
            FROM
                books b
                    INNER JOIN
                bookcopies bc ON b.bookid = bc.bookid
                    INNER JOIN
                loans l ON bc.bookcopyid = l.bookcopyid
                    INNER JOIN
                borrowers br ON l.borrowerid = br.borrowerid
            ORDER BY br.familyname , br.firstname , l.loandate;"""
    connection.execute(sql)
    loanList = connection.fetchall()
    return loanList


def search_func(searched, type):

    connection = getCursor()
    where_clause = ""

    if type == 1:
        where_clause = f"booktitle LIKE '%{searched}%'"
    elif type == 2:
        where_clause = f"author LIKE '%{searched}%'"
    else:
        where_clause = f"booktitle LIKE '%{searched}%' OR author LIKE '%{searched}%'"

    sql = """SELECT * FROM books WHERE {}""".format(where_clause)
    connection.execute(sql)
    searched_list = connection.fetchall()
    return searched_list


def bookcopies_func(book_id):
    connection = getCursor()
    sql = """ SELECT 
                bc.bookcopyid, bc.format, l.returned, MAX(l.loandate)
            FROM
                bookcopies bc
                    INNER JOIN
                books b ON bc.bookid = b.bookid
                    LEFT JOIN
                loans l ON bc.bookcopyid = l.bookcopyid
            WHERE
                b.bookid = {}
            GROUP BY bc.bookcopyid
            ORDER BY l.loandate;""".format(book_id)
    connection.execute(sql)
    bookcopies = connection.fetchall()
    connection.execute(
        "select booktitle, author from books where bookid = {}".format(book_id))
    booktitle = connection.fetchall()
    return bookcopies, booktitle


def searchBorrowers_func(searched, type):
    connection = getCursor()
    sql = ""
    if type == "Name":
        sql = """ SELECT 
                    borrowers.borrowerid,
                    CONCAT(borrowers.firstname,
                            ' ',
                            borrowers.familyname),
                    borrowers.dateofbirth,
                    borrowers.housenumbername,
                    borrowers.street,
                    borrowers.town,
                    borrowers.city,
                    borrowers.postalcode
                FROM
                    borrowers
                WHERE
                    CONCAT(firstname, ' ', familyname) LIKE '%{}%'
                        OR familyname LIKE '%{}%'""".format(
            searched, searched)
    if type == "ID":
        sql = """ SELECT * FROM borrowers WHERE borrowerid = {} """.format(
            searched)

    connection.execute(sql)
    borrowers = connection.fetchall()

    return borrowers


def updateBorrower_func(
        id, firstname=None, lastname=None, DoB=None, house=None, street=None, town=None, city=None, postcode=None):

    update_list = {
        "firstname": firstname, "familyname": lastname,
        "dateofbirth": DoB, "housenumbername": house,
        "street": street, "town": town,
        "city": city, "postalcode": postcode}

    if all(item is None or item == "" for item in update_list.values()):
        return 500
    sql = """UPDATE borrowers SET """

    for field, key in update_list.items():
        if key != "" and key is not None:
            sql += f"{field} = '{key}', "

    sql = sql.strip(', ')
    sql += f" WHERE borrowerid = {id}"
    

    print(sql)

    connection = getCursor()

    connection.execute(sql)
    borrowers = connection.fetchall()

    return 200


def createBorrower_func(
        firstname=None, lastname=None,
        DoB=None, house=None, street=None,
        town=None, city=None, postcode=None):

    update_list = {
        "firstname": firstname, "familyname": lastname,
        "dateofbirth": DoB, "housenumbername": house,
        "street": street, "town": town,
        "city": city, "postalcode": postcode}
    sql = "INSERT INTO borrowers ("
    values = " VALUES ( "
    for field, key in update_list.items():
        print(sql + values)
        if key == "" or key is None:
            return 500
        sql += f"{field}, "
        values += f"'{key}', "
    sql, values = sql.strip(', '), values.strip(', ')
    sql += ") "
    values += ")"

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
    sql = """SELECT 
                title, bookid AS ID, SUM(Times) AS loantimes
            FROM
                (SELECT 
                    b.booktitle AS title,
                        b.bookid AS bookid,
                        COUNT(bc.bookcopyid) AS Times
                FROM
                    bookcopies bc
                LEFT JOIN loans l ON bc.bookcopyid = l.bookcopyid
                INNER JOIN books b ON bc.bookid = b.bookid
                GROUP BY bc.bookcopyid) AS cpt
            GROUP BY bookid
            ORDER BY bookid;"""

    connection = getCursor()
    connection.execute(sql)
    table = connection.fetchall()

    return table


def borrowersummary_func():
    sql = """SELECT 
                br.borrowerid AS ID,
                br.firstname,
                br.familyname,
                COUNT(l.borrowerid) AS loans
            FROM
                borrowers br
                    LEFT JOIN
                loans l ON br.borrowerid = l.borrowerid
            GROUP BY br.borrowerid;"""

    connection = getCursor()
    connection.execute(sql)
    table = connection.fetchall()

    return table

