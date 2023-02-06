# COMP636_web_app

`Lu-Yung Huang 1154980

## run as development mode on localhost
```sh
$ flask run
```

## Report

This report will focus on 3 points:
- The overall strutral ideas in implementing this web app, a library management system.
- Assumptions and design ideas
- A discussion that outlines what changes would be required if this application was to support multiple library branches.


### The structure of the solution



    │   ├── templates
    │   │   ├── base.html
    │   │   ├── forms.py
    │   │   ├── models.py
    │   │   ├── templates
    │   │   │   └── auth
    │   │   │       ├── index.html
    │   │   │       ├── macros.html
    │   │   │       ├── profile.html
    │   │   │       └── settings.html
    │   │   └── views.py

