from flask import Blueprint, render_template, request, flash, redirect, url_for,before_render_template
from .models import user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = user.query.filter_by(email=email).first()
        if existing_user:
            if check_password_hash(existing_user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(existing_user, remember=True)
                
                return render_template("Home.html")
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", existing_user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1') 
        password2 = request.form.get('password2')

        existing_user = user.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.', category='error')
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = user(email=email, name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return render_template("login.html", existing_user=current_user)

    return render_template("sign_up.html", existing_user=current_user)

@auth.before_app_request
def before_app_request():
    if current_user.is_authenticated:
            logout_user()