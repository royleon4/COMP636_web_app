from flask import Flask
from webforms import SearchBookForm
import public, staff

app = Flask(__name__)

# Secret Key!
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

# Pass stuff to Nav Bar
@app.context_processor
def base():
    form = SearchBookForm()
    return dict(SearchBookForm=form, staff='staff')

"""For Public access"""

app.add_url_rule('/', view_func=public.home)
app.add_url_rule('/listbooks', view_func=public.listbooks)
app.add_url_rule('/search', view_func=public.search, methods=['POST'])
app.add_url_rule('/bookcopies/<int:book_id>', view_func=public.bookcopies)

"""for Staff access"""

pstaff = '/staff'

app.add_url_rule('/staff', view_func=staff.staff)
app.add_url_rule(f'{pstaff}/listbooks', view_func=staff.stafflistbooks)
app.add_url_rule(f'{pstaff}/loanbook', view_func=staff.staffloanbook)
app.add_url_rule(f'{pstaff}/loan/add', view_func=staff.addloan, methods=['POST'])
app.add_url_rule(f'{pstaff}/listborrowers', view_func=staff.listborrowers)
app.add_url_rule(f'{pstaff}/currentloans', view_func=staff.staffcurrentloans)
app.add_url_rule(f'{pstaff}/overdueloans', view_func=staff.overdueloans)
app.add_url_rule(f'{pstaff}/search', view_func=staff.staffsearch, methods=['POST'])
app.add_url_rule(f'{pstaff}/bookcopies/<int:book_id>', view_func=staff.staffbookcopies)
app.add_url_rule(f'{pstaff}/listborrowers', view_func=staff.searchBorrowers, methods=['POST'])
app.add_url_rule(f'{pstaff}/borrower/<int:borrower_id>', view_func=staff.updateBorrowerForm)
app.add_url_rule(f'{pstaff}/borrower/update/<int:borrower_id>', view_func=staff.updateBorrower, methods=['POST'])
app.add_url_rule(f'{pstaff}/newborrower', view_func=staff.newBorrower)
app.add_url_rule(f'{pstaff}/borrower/create', view_func=staff.createBorrower, methods=['POST'])
app.add_url_rule(f'{pstaff}/loan/return/<int:borrowerid>&<int:bookid>', view_func=staff.loanreturn, methods=['POST'])

app.add_url_rule(f'{pstaff}/summary/book', view_func=staff.loansummary)
app.add_url_rule(f'{pstaff}/summary/borrower', view_func=staff.borrowersummary)






