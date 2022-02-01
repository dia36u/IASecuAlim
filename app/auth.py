from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['POST','GET'])
def identification():
        if request.method == 'POST':
                email = request.form.get('email')
                password = request.form.get('password')
                user = User.query.filter_by(email=email).first()
                if user:
                        if check_password_hash(user.password, password):
                                flash('Identification réussi!', category='info')
                        else: flash('Incorrect password, try again.', category='error')
                else: flash('Email does not exist.', category='error')
        return render_template("auth/identification.html")


@auth.route('/signup', methods=['POST','GET'])
def signup():
        if request.method == 'POST':
                email = request.form.get('email')
                first_name = request.form.get('firstName')
                password1 = request.form.get('password1')
                password2 = request.form.get('password2')
                
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash('Account created!', category='success')
                return redirect(url_for('views.profil'))
        return render_template("auth/sign_up.html")