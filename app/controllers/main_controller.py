from flask import render_template
from base_controller import BaseController

class MainController(BaseController):
    def index(self, request=None):
        return render_template('main/index.html')

    def map(self, id, request, params={}):
        form = params['form']
        return render_template('main/map.html', form=form)
