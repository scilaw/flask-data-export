
from flask.ext.security import Security, SQLAlchemyUserDatastore
from app import db
from .models import Role, User

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)


def find_or_create_user(email):
    user = security.datastore.find_user(email=email)
    if (user is None):
        user = security.datastore.create_user(email=email)
        db.session.commit()
    return user
