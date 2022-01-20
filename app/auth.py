from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['POST','GET'])
def identification():
        if request.method == 'POST':
                name = request.form.get('name')
                pswd = request.form.get('pswd')
                flash('Identification réussi!', category='info')
                return render_template("views/user_profil.html")
        return render_template("auth/identification.html")


    