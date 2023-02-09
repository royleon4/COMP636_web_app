from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length

# A Search Form to search books
class SearchBookForm(FlaskForm):
	searched = StringField("Searched", render_kw={"placeholder": "Search Books!"}, validators=[DataRequired()])
	searchedType = SelectField("Type", choices=[ ("All", "All"), ("Title", "Title"), ("Author", "Author")], validators=[DataRequired()], default="All")
	submit = SubmitField("Search")

class SearchBorrowersForm(FlaskForm):
	searchedBorrowers = StringField("Search Borrowers", render_kw={"placeholder": "Search Borrowers!"}, validators=[DataRequired()])
	selectedTypeRadio = RadioField("Type", choices=[("Name", "Name"), ("ID", "ID")], validators=[DataRequired()], default="Name")
	submit = SubmitField("submit")

class AddLoanForm(FlaskForm):
	borrower = SelectField("Borrower", choices=[("","Pick a borrower!")], validate_choice=False, validators=[DataRequired()], default="")
	book = SelectField("Book", choices=[("","Pick a Book Copy!")], validate_choice=False, validators=[DataRequired()], default="", )
	submit = SubmitField("submit")

class UpdateBorrowerForm(FlaskForm):

	firstname = StringField("First Name", render_kw={"placeholder": "First Name"}, validators=[Length(min=0, max=25)])
	familyname = StringField("Family Name", render_kw={"placeholder": "Family Name"})
	dateofbirth = DateField('Date of Birth')
	housenumber = StringField('House Number', render_kw={"placeholder": "House Number / Name"})
	street = StringField("Street", render_kw={"placeholder": "Street"})
	town = StringField("Town", render_kw={"placeholder": "Town"})
	city = StringField("City", render_kw={"placeholder": "City"})
	postcode = IntegerField("Postal Code", render_kw={"placeholder": "Postal Code", "type" : "number"})
	submit = SubmitField("submit")

class CreateBorrowerForm(FlaskForm):

	firstname = StringField("First Name", render_kw={"placeholder": "First Name"}, validators=[Length(min=0, max=25), DataRequired()])
	familyname = StringField("Family Name", render_kw={"placeholder": "Family Name"}, validators=[Length(min=0, max=25), DataRequired()])
	dateofbirth = DateField('Date of Birth', validators=[ DataRequired()])
	housenumber = StringField('House Number', render_kw={"placeholder": "House Number / Name"}, validators=[Length(min=0, max=25), DataRequired()])
	street = StringField("Street", render_kw={"placeholder": "Street"}, validators=[Length(min=0, max=25), DataRequired()])
	town = StringField("Town", render_kw={"placeholder": "Town"}, validators=[Length(min=0, max=25), DataRequired()])
	city = StringField("City", render_kw={"placeholder": "City"}, validators=[Length(min=0, max=25), DataRequired()])
	postcode = IntegerField("Postal Code", render_kw={"placeholder": "Postal Code", "type" : "number"}, validators=[DataRequired()])
	submit = SubmitField("submit")
