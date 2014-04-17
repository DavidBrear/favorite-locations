from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required

from app.models import User

class LoginForm(Form):
    openid = TextField('openid')
    remember_me = BooleanField('remember_me', default=False)
    email = TextField('email')
    password = PasswordField('password')

class LocationForm(Form):
    name = TextField('name', validators= [Required()])
    latitude = TextField('latitude', validators= [Required()])
    longitude = TextField('longitude', validators= [Required()])
    address = TextField('address', validators= [Required()])

class RegisterForm(Form):
    email = TextField('email', validators= [Required()])
    password = PasswordField('password', validators= [Required()])
    password_confirm = PasswordField('password_confirm', validators= [Required()])

    def validate(self):
        if not Form.validate(self):
            return False
        if self.password.data != self.password_confirm.data:
            self.password.errors.append('Password does not match confirm')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user != None:
            self.email.errors.append('That email is already in the system')
            return False
        return True

class EditForm(Form):
    nickname = TextField('nickname', validators=[Required()])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use please pick another')
            return False
        return True
