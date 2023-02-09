# COMP636_web_app

`Lu-Yung Huang 1154980

## run as development mode on localhost
```sh
$ flask run
```

## Report

This report will focus on 3 points:
- The overall strutral ideas in implementing this web app, a library management system.
    Outlining the structure of your solution (routes & functions). This should be brief, but be sure to indicate how your routes and templates relate to each other and what data is being passed between them, do not just give a list of your routes.
- Assumptions and design ideas
    Detailing any assumptions and design decisions that you have made. For example, did you share a page template between public and staff or use two separate pages? Did you detect GET or POST method to determine what page displays? If so, how and why? Note these types of decisions and assumptions as you work.
- A discussion that outlines what changes would be required if this application was to support multiple library branches.
    Changes required to database tables (new tables and modifications to existing tables)
    Changes required to the design and implementation of your web app.



### The structure of the solution

- In overall, this web app has got two major routes: 
    - base route of "/" for public access and another route , 
        - Contains functions to public usages (read only instead of editing)
    - "/staff", for staff members to access
        - contains functions to internal usages (support both read and write to the database)

- Each route handles different functionalities


    - Public assess  ("/")

        | Routes | Method| Template |
        | ----------- | -----| ----|
        | /listbooks  <br /> /bookcopy/{book id}| Get|booklist.html <br /> bookcopies.html|
        |/search|Post| search.html|

        1. Each book is linked to their page of all copies 
        2. The search page is fixed on the navbar, so users can search whenever they want to. 
        3. navbar is the base page and is extended by the templates above
        

    - Staff access ("/staff")

        Inherited from Public access with prefix ("/staff") and has extra following features:
        
        Loan Books
        | Routes | Method| Template |
        | ----------- | -----| ---|
        | /loanbook | Get| addloan.html|
        | /loan/add | Post | redirects to currentloans.html|
        | /loan/return/{borrowerid} & {bookid} | Post | currentloans.html |
        

        1. **/loanbook** is linked to addloan.html, shows a form users can choose the borrower and a book copy.
        2. Once the form is submitted, the route **/loan/add** is activated and redirects to **/staff/currentloans** to show the changes. (tmplate currentloans.html)
        3. **loan/return/ {borrowerid} & {bookid}**, an action to return the chosen row of book copy, and will reload the currentloan.html page to see the changes.
        

        ---
        Borrowers 
        | Routes | Method| Template |
        | ----------- | -----| ---|
        | /listborrowers | Get| borrowerlist.html|
        | /borrower/{borrower_id} | Get | updateborrower.html|
        | /borrower/update/{borrower_id} | Post | redirects to borrowerlist.html|
        | /newborrower | Get | newborrower.html|
        | /borrower/create | Post | redirects to borrowerlist.html|
        

        1. **/listborrowers** lists all borrowers on borrowerlist page.
        2. **/borrower/{borrower_id}** and **/newborrower** show the form for the user to type in in order to make changes, once they hit the submit button on those two pages, Post action of /borrower/update/{borrower_id} or /borrower/create will be activated and redirects to borrowerlist.html page to see the changes immediately.

        ---

        Summary 
        | Routes | Method| Template |
        | ----------- | -----| ---|
        | /summary/book | Get| bookcummary.html|
        | /summary/borrower | Get | borrowersummary.html|
        | /overdueloans | Get | overdueloans.html |
        

        1. **/summary/book** lists all book with number of times they have been on loan.
        2. **/summary/borrower** lists all borrowers with number of times they have loaned.
        3. **/overdueloans** shows overdueloans.html that contains books that are overdued in a table.

### Assumptions and design ideas

- Some templates are shared becuase there are a lot of common information such as **/listbooks** and **/staff/listbooks**. their template is shared however, a slight difference is shown on the staff page. 
- My overall design idea is to utilize Model, View , Controler throughout the code design. Hence, the original app.py was split into 4 parts, app, features, public, and staff.

    - features.py
        - Acts like model in this webapp. The only job it does it to interact with database and send data to controllers.
        - This file should only import sql related libraries and use sql queries.
        - The functions in this file are meant to be reusable, so they could be reused by other function when needed. The usability in this python file is important.

    - public.py and staff.py
        - They both act like controllers in this webapp. 
        - the reason of having two controllers is to have better data flow and avoid them to communicate to each other while the code is implemented. 
        - public.py only worries about how to process data to public users and staff.py only worry about the functionalities for internal users. 
    - app.py
        - acts like the medium, or a router to wire everything up, so in this file we can see all the routes and their related templates. 
        - we may add validator or middleware here in the future if it is needed to create more data safety and avoid some security issues. 
- Webforms 
    - webform has been used because I assumed there should be a lot of forms(or fields), therefore I needed one place that allow me to change the requirements of each datafield. 
    - webform sucessfully solved the problem and I believe its good to use this to achieve a cleaner code and its also an extension of Flask, so it's not out of the allowed techonlogies scope.
- Rusable templates
    - Some templated share partial contents, but not totally identical, so I decided to take out the identical part and then include them when needed. 
        - booktable.html will only returns the table of books, so it can be used (included) by booklist.html, search.html. Therefore, once there is a need to modify the table, booktable.html is the only place needs modifications. 
- content based on the URL
    - There is a page the content shows differently but they share the same template. It's using the conditional statement from jinja to decide what content to show because there are two different authorities in this webapp, so jinja helps a lot to show different content on the same page. 
    - e.g. loan times will only show via **/staff/listbooks**

### A discussion that outlines what changes would be required if this application was to support multiple library branches.

- Database
    - A new table should be created called library or anything alike (e.g. branch) with the primary key of their unique code.
    - Bookcopies table may need to have new column of location to indicate which branch this book is at. 
    - Each table may need to have a branch colunm as foreign keys to indicate where they are (registered, borrowed, stored) from except the book table because it only contains general information of one book.
    - Each branch can even have their own tables from the current database (copying the models of database on each branch), but the communication between branch will be difficult. However, the question didn't specify if they need to communicate to each other, so it is a possible solution, too.
    
- Design and implementation
    - There are many possible solutions to implement llibrary branches, and it will heavily depend on what is needed, so the following is just assumptions but not ideal as we cannot talk to any clients. 
        1. We may design a home page that have multiple routes and each links to different branch, and the rest stays the same. Each branch can only search books on that particular branch.
        2. Each loan might need to add a new column of which branch the book is borrowed from and shown on the table or graph, the staff should be able to return a book and also specify the location if the user may return the copy to different branches. 
        3. The search engine can indicate or filter the branch before searching for books copies.
