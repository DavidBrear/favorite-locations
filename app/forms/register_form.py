from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required

from app.models import User

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
