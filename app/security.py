
from flask_security import Security, SQLAlchemyUserDatastore
from app import db
from .models import Role, User

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)

def find_or_create_user(email):
    print(email)

    #user = security.datastore.find_user(email=email)
    user = user_datastore.find_user(email=email)
    print(user)
    if (user is None):
        #user = security.datastore.create_user(email=email)
        user = user_datastore.create_user(email=email)

	print(user)
        db.session.commit()
    return user
