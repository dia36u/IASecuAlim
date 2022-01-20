from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/etablissement')
def etablissement():
    return render_template("view/add_etablissement.html")
