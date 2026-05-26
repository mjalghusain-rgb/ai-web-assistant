from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models.user import User

from database.db import db

import re



# =========================================
# BLUEPRINT
# =========================================

auth = Blueprint(
    "auth",
    __name__
)



# =========================================
# PASSWORD VALIDATION
# =========================================

def validate_password(password):

    if len(password) < 6:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    if re.search(r"[^A-Za-z0-9]", password):
        return False

    return True



# =========================================
# REGISTER
# =========================================

@auth.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]


        if not validate_password(password):

            flash("""
Password must:
- Be at least 6 characters
- Include one uppercase letter
- Include one number
- No symbols allowed
""")

            return redirect("/register")


        existing_user = (
            User.query.filter_by(
                email=email
            ).first()
        )


        if existing_user:

            flash(
                "Email already exists."
            )

            return redirect("/register")


        hashed_password = (
            generate_password_hash(
                password
            )
        )


        is_first_user = (
            User.query.count() == 0
        )


        user = User(

            username=username,

            email=email,

            password=hashed_password,

            is_admin=is_first_user
        )


        db.session.add(user)

        db.session.commit()


        flash(
            "Account created successfully."
        )

        return redirect("/login")


    return render_template(
        "register.html"
    )



# =========================================
# LOGIN
# =========================================

@auth.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]


        user = (
            User.query.filter_by(
                email=email
            ).first()
        )


        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect("/")


        flash(
            "Invalid email or password."
        )


    return render_template(
        "login.html"
    )



# =========================================
# LOGOUT
# =========================================

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")
