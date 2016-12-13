from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension


def get_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('app.cfg')
    return app


def get_db(app):
    with app.app_context():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = SQLAlchemy(app)
            return db


def create_app():
    global app
    from .security import security
    security.init_app(app)
    from .views import views
    blueprints = [views]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    return app


app = get_app()
db = get_db(app)
mail = Mail(app)
migrate = Migrate(app, db)
debug_bar = DebugToolbarExtension(app)
