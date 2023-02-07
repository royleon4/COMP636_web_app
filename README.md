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

- In overall, this web app has got two major routes base route of "/" for public access and another route for staff members to access, "/staff". 

- Each route handles different functionalities, one for external users and another one for internal users. 

- For public routes there are

-- "/", for home page
-- "/listbooks"


