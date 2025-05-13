
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_bcrypt import Bcrypt
from flask import redirect, url_for, session
from models.user import User

login_manager = LoginManager()
bcrypt = Bcrypt()

def init_login(app):
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    bcrypt.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.active and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return True
    return False

def logout_current_user():
    logout_user()
    session.pop('user_id', None)
