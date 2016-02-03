from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension


def get_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('app.cfg')
    return app


# TODO: use flask.g - http://flask.pocoo.org/docs/0.10/appcontext/#app-context
def get_db():
    app = get_app()
    return SQLAlchemy(app)


db = get_db()


def create_app():
    app = get_app()
    Migrate(app, db)
    DebugToolbarExtension(app)
    from .security import security
    security.init_app(app)
    from .views import views
    blueprints = [views]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    return app
