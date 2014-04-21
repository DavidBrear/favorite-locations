from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json, abort
from .. import BaseController

from app.models import Location
from app.forms import LocationForm
from app import db

class APILocationController(BaseController):

    def delete(self, id):
        location = g.user.locations.filter_by(id=id).first()
        db.session.delete(location)
        db.session.commit()
        return json.dumps({'success': True})
    def index(self):
        locations = g.user.locations.all()
        return json.dumps([i.serialize for i in locations])
        #return render_template('api/locations/index.json', locations=locations)

    def create(self, request):
        form = LocationForm()
        location = Location(name = form.name.data, address = form.address.data, latitude=form.latitude.data, longitude=form.longitude.data, creator = g.user)
        db.session.add(location)
        db.session.commit()
        return json.dumps(location.serialize)
        #return render_template('api/locations/show.json', location=location)

    def show(self, id):
        location = g.user.locations.filter_by(id = id).first()
        if location is None:
            return '{"forbidden": "You cannot view this page"}', 403
        return json.dumps(location.serialize)
        #return render_template('api/locations/show.json', location=location)
