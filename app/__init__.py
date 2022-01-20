from flask import Flask

def create_app():
    app = Flask(__name__)

    # Define Flask configuration
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'test'

    # Define route with Blueprint
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app




