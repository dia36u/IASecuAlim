from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['POST','GET'])
def identification():
        if request.method == 'POST':
                mail = request.form.get('email')
                pswd = request.form.get('password')

                return render_template("views/user_profil.html")



    