# For authentication
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from . import db
from .models import User


basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify(username, password):
    user = db.session.execute(db.select(User).where(User.username==username)).scalar_one_or_none()
    if user is not None and user.check_password(password):
        return user
    return None