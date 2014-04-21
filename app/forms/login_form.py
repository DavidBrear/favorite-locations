from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required

class LoginForm(Form):
    openid = TextField('openid')
    remember_me = BooleanField('remember_me', default=False)
    email = TextField('email')
    password = PasswordField('password')
