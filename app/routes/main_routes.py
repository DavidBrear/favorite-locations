from app import app
from flask import request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.controllers import MainController
from app.forms import LocationForm

@app.route('/')
def index():
    return MainController().call(request)

@app.route('/map')
@login_required
def map():
    form = LocationForm()
    return MainController().call(request, action='map', params={'form': form})
