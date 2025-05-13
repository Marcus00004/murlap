from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'nagyonbiztonsagoskulcs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- IMPORTOK ---
from user_auth_admin import *
from routes.partners import *
from routes.form_definitions import init_form_routes

# az app példány létrehozása után:
init_form_routes(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
