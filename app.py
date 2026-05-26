from flask import (
    Flask,
    render_template
)

from flask_login import (
    LoginManager,
    login_required,
    current_user
)

from dotenv import load_dotenv

from database.db import db

from models.user import User

from routes.auth import auth

from routes.ai_routes import (
    ai_routes
)

from routes.profile_routes import (
    profile_routes
)

from routes.admin_routes import (
    admin_routes
)

from routes.upload_routes import (
    upload_routes
)

import os



# =========================================
# LOAD ENV
# =========================================

load_dotenv()



# =========================================
# CREATE FLASK APP
# =========================================

app = Flask(__name__)

app.secret_key = (
    "super_secret_v3_key"
)



# =========================================
# DATABASE CONFIG
# =========================================

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///users.db"

app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False



# =========================================
# UPLOAD CONFIG
# =========================================

app.config[
    "UPLOAD_FOLDER"
] = "static/uploads"



# =========================================
# INIT DATABASE
# =========================================

db.init_app(app)



# =========================================
# LOGIN MANAGER
# =========================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = (
    "auth.login"
)



# =========================================
# USER LOADER
# =========================================

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(
        int(user_id)
    )



# =========================================
# REGISTER BLUEPRINTS
# =========================================

app.register_blueprint(auth)

app.register_blueprint(ai_routes)

app.register_blueprint(profile_routes)

app.register_blueprint(admin_routes)

app.register_blueprint(upload_routes)



# =========================================
# HOME PAGE
# =========================================

@app.route("/")
@login_required
def home():

    return render_template(

        "index.html",

        username=current_user.username,

        user=current_user
    )



# =========================================
# CREATE DATABASE
# =========================================

with app.app_context():

    db.create_all()



# =========================================
# START APP
# =========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False
    )
