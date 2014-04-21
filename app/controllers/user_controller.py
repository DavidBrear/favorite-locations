from flask import render_template
from base_controller import BaseController

from app.models import User

class UserController(BaseController):
    def index(self, request=None):
        return render_template('/users/index.html')

    def show(self, id):
        user = User.query.filter_by(id=id).first()
        return render_template('/users/show.html', user=user);

