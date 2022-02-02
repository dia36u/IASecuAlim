from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['POST','GET'])
def login():
        if request.method == 'POST':
                email = request.form.get('email')
                password = request.form.get('password')
                user = User.query.filter_by(email=email).first()
                if user:
                        if check_password_hash(user.password, password):
                                flash('Identification réussi!', category='info')
                                login_user(user, remember=True)
                                return redirect(url_for('views.profil'))
                        else: flash('Mot de passe incorrect!', category='error')
                else: flash("l'email n'existe pas", category='error')
        return render_template("auth/login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['POST','GET'])
def signup():
        if request.method == 'POST':
                email = request.form.get('email')
                first_name = request.form.get('firstName')
                password1 = request.form.get('password1')
                password2 = request.form.get('password2')
                
                user = User.query.filter_by(email=email).first()
                if user:
                        flash("l'email existe déjà.", category='error')
                elif len(email) < 4:
                        flash("L'email doit contenir plus de 3 caractères.", category='error')
                elif len(first_name) < 2:
                        flash("Le nom doit contenir plus d'un caractère", category='error')
                elif password1 != password2:
                        flash('les mots de passe sont différents.', category='error')
                elif len(password1) < 5:
                        flash('le mot de passe doit contenir 5 caractères minium.', category='error')
                else:
                        new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                        password1, method='sha256'))
                        db.session.add(new_user)
                        db.session.commit()
                        login_user(new_user, remember=True)
                        flash('Compte créé', category='success')
                        return redirect(url_for('auth.login'))
        return render_template("auth/sign_up.html", user=current_user)