from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, EditForm, RegisterForm, LocationForm
from models import User, Location, ROLE_USER, ROLE_ADMIN

from hashlib import md5
import random

from datetime import datetime

@app.before_request
def before_request():
    g.user = current_user

    if g.user.is_authenticated():
        g.user.last_login = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == '':
        flash('Invalid login. Please try again')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()

    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]

        nickname = User.make_unique_nickname(nickname)
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

# ROUTES
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    form = LocationForm()
    return render_template('index.html',
            title = 'Home',
            form = form,
            locations= user.locations,
            user = user)

@app.route('/api/locations', defaults={'id': None}, methods=['POST', 'GET'])
@app.route('/api/locations/<id>', methods=['POST', 'GET'])
@login_required
def api_locations(id):
    form = LocationForm()
    if id is None:
        if request.method.lower() == 'get':
            locations = g.user.locations.all()
            return json.dumps([i.serialize for i in locations])
        location = Location(name = form.name.data, address = form.address.data, latitude=form.latitude.data, longitude=form.longitude.data, owner = g.user)
        db.session.add(location)
        db.session.commit()
        return json.dumps(location.serialize)
    else:
        location = g.user.locations.query.filter_by(id = id).first()
        if request.method.lower() == 'get':
            return json.dumps(location.serialize)
        if request.form['method'] == 'delete':
            db.session.delete(location)
            db.session.commit()
            return json.dumps({})

    return jsonify({'sorry': 'something went wrong'})




@app.route('/login', methods=['POST', 'GET'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        if form.email.data is not None:
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.authenticate(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Invalid email/password')
        else:
            return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html',
            title = 'Sign In',
            providers = app.config['OPENID_PROVIDERS'],
            form = form)

@app.route('/edit', methods=['POST', 'GET'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        db.session.add(g.user)
        db.session.commit()
        flash('Saved your changes')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname

    return render_template('edit.html',
            form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('Could not find a user with the nickname ' + nickname)
        return redirect(url_for('index'))
    return render_template('user.html',
            locations = user.locations.all(),
            user = user)
@app.route('/register', methods= ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        nickname = User.make_unique_nickname(form.email.data.split('@')[0])
        password_salt = User.generate_password_salt()
        password_digest = User.generate_password_digest(form.password.data, password_salt)
        user = User(nickname=nickname, email = form.email.data, password_salt = password_salt, password_digest=password_digest)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form, title='Register for Uber Favorites')

@app.route('/locations/<action>', defaults={'id': None}, methods= ['GET', 'POST'])
@app.route('/locations/<action>/<id>', methods= ['GET', 'POST'])
def locations(action, id):
    print request.form
    form = LocationForm()
    if form.validate_on_submit() and action == 'create':
        location = Location(latitude=form.latitude.data, longitude=form.longitude.data, creator=g.user, name=form.name.data, address=form.address.data)
        db.session.add(location)
        db.session.commit()
        print 'saved'
        return jsonify( {
            'error': None,
            'id': location.id,
            'name': location.name,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'address': location.address
            }), 200
    if action == 'delete':
        location = g.user.locations.filter_by(id = id).first();
        if location is None:
            return jsonify({'error': 'could not find that location to delete'}), 401
        db.session.delete(location)
        db.session.commit()
        return jsonify({'error': None})
    return jsonify({
        'error': 'something went wrong saving the location'
        }), 401


#ERROR PAGES
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
