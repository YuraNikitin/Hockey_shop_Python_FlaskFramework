from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user

from app import app
from app import db
from app.forms.user import LoginForm, RegistrationForm, EditProfileForm
from app.models.user import User


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("SORRY Invalid password or username")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('User/login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data, name=form.name.data, surname=form.surname.data,email=form.email.data,
            address=form.address.data, role_id=2
        )

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("GREAT your are now registered user!")
        return redirect(url_for('login'))

    return render_template('User/register.html', title='Register', form=form)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('User/user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():

    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        db.session.commit()
        flash("Great your changes are saved!")
        return redirect(url_for('user', username=current_user.username))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.email.data = current_user.email
        form.address.data = current_user.address

    return render_template('User/edit_profile.html', title='Edit profile', form=form)
