from flask import render_template
from app.controllers import BaseController

class LocationController(BaseController):

    def index(self):
        return render_template('/location/index.html')

    def show(self, id):
        return render_template('/location/show.html')

