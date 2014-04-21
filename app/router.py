from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
import routes
from datetime import datetime
from app.models import User

@app.before_request
def before_request():
    g.user = current_user

    if g.user.is_authenticated():
        g.user.last_login = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

