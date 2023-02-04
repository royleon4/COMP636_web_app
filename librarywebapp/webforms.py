from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea

# A Search Form to search books
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")

class SearchBorrowersForm(FlaskForm):
	searchedBorrowers = StringField("searchedBorrowers", validators=[DataRequired()])
	selectedType = SelectField("selectedType",coerce=str, choices=["Name", "ID"],  validators=[DataRequired()])
	submit = SubmitField("submit")


class updateBorrowerForm(FlaskForm):

	firstname = StringField("firstname")
	familyname = StringField("familyname")
	dateofbirth = DateField('dob', format='%Y-%M-%D')
	housenumber = StringField('housenname')
	street = StringField("street")
	town = StringField("town")
	city = StringField("city")
	postcode = StringField("postcode")
	submit = SubmitField("submit")

class createBorrowerForm(FlaskForm):

	firstname = StringField("firstname")
	familyname = StringField("familyname")
	dateofbirth = DateField('dob', format='%Y-%M-%D')
	housenumber = StringField('housenname')
	street = StringField("street")
	town = StringField("town")
	city = StringField("city")
	postcode = StringField("postcode")
	submit = SubmitField("submit")
