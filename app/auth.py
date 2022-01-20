from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/')
def identification():
        return render_template("auth/identification.html")


    