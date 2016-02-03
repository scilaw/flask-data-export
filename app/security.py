
from flask.ext.security import Security, SQLAlchemyUserDatastore
from app import db
from .models import Role, User

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)
