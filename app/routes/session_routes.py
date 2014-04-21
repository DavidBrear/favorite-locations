from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User

@app.route('/login', methods=['POST', 'GET'])
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
                return redirect(url_for('map'))
            else:
                flash('Invalid email/password')
    return render_template('/session/login.html',
            title = 'Sign In',
            form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

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
    return render_template('/session/register.html', form=form, title='Register for Uber Favorites')
