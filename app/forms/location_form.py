from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required

class LocationForm(Form):
    name = TextField('name', validators= [Required()])
    latitude = TextField('latitude', validators= [Required()])
    longitude = TextField('longitude', validators= [Required()])
    address = TextField('address', validators= [Required()])
