from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask.ext.login import login_required
from app import app
from app.controllers.api import APILocationController

@app.route('/api/locations', defaults={'id': None, 'action':None}, methods=['GET', 'POST'])
@app.route('/api/locations/<id>', defaults={'action':None}, methods=['GET', 'POST'])
@app.route('/api/locations/<id>/<action>', methods=['GET', 'POST'])
@login_required
def api_locations(id, action):
    return APILocationController().call(request, id, action)
