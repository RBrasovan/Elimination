from flask import render_template, session, redirect, request, url_for, flash
from flask_login import login_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm
from .forms import RegistrationForm
from flask_login import logout_user, login_required

@auth.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			print(user)
			session['username']=user.username
			print(session['username'])
			nextURL = request.args.get('next')
			if nextURL is None or not nextURL.startswith('/'):
				nextURL = url_for('main.start')
			return redirect(nextURL)
		flash('Invalid username or password.')
	return render_template('auth/login.html', form=form)

@auth.route('/register',methods=['GET','POST'])
def register():
	form=RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,username=form.username.data,password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You can now login')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html',form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	session['username']=''
	flash('You have been logged out')
	return redirect(url_for('main.index'))
