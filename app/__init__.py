from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from os import path

db = SQLAlchemy()
DB_NAME= "database.db"

def create_app():
    app = Flask(__name__)

    # Define Flask configuration
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'test'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Define route with Blueprint
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

<<<<<<< HEAD
=======
    from .models import User, Estimation

    create_database(app)

    return app

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
>>>>>>> 4449505dac3893f5cdba4e5b0b9ecc09044a798d

    return app

