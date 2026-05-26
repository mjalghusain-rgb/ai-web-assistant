from flask import Flask, render_template, request, jsonify, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from dotenv import load_dotenv

import openai
import os
import re


# =========================
# LOAD ENV
# =========================

load_dotenv()


# =========================
# FLASK CONFIG
# =========================

app = Flask(__name__)

app.secret_key = "supersecretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

db = SQLAlchemy(app)


# =========================
# LOGIN MANAGER
# =========================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


# =========================
# OPENAI
# =========================

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =========================
# USER MODEL
# =========================

class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(
        int(user_id)
    )


# =========================
# PASSWORD VALIDATION
# =========================

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


# =========================
# HOME
# =========================

@app.route("/")
@login_required
def home():

    return render_template(
        "index.html",
        username=current_user.username
    )


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]


        if not validate_password(password):

            flash("""
Password must:
- Be at least 6 characters
- Contain one uppercase letter
- Contain one number
- No symbols allowed
""")

            return redirect("/register")


        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash("Email already exists.")

            return redirect("/register")


        hashed_password = generate_password_hash(
            password
        )

        is_first_user = User.query.count() == 0


        user = User(
            username=username,
            email=email,
            password=hashed_password,
            is_admin=is_first_user
        )

        db.session.add(user)

        db.session.commit()

        flash("Account created successfully.")

        return redirect("/login")

    return render_template(
        "register.html"
    )


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect("/")

        flash("Invalid email or password.")

    return render_template(
        "login.html"
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")


# =========================
# MAIN CHAT API
# =========================

@app.route("/chat", methods=["POST"])
@login_required
def chat():

    data = request.json

    user_message = data["message"]

    try:

        response = client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",

                    "content": f"""
You are an advanced AI DevOps assistant.

The current user is:
{current_user.username}

Help with:
- Linux
- AWS
- Docker
- Networking
- Security
- DevOps
- Resume generation
- Interview preparation

Be professional and helpful.
"""
                },

                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        ai_response = (
            response
            .choices[0]
            .message
            .content
        )

        return jsonify({
            "response": ai_response
        })

    except Exception as e:

        return jsonify({
            "response": str(e)
        })


# =========================
# INTERVIEW EVALUATION
# =========================

@app.route("/evaluate-interview", methods=["POST"])
@login_required
def evaluate_interview():

    data = request.json

    question = data["question"]

    answer = data["answer"]

    try:

        response = client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",

                    "content": """
You are a professional technical interviewer.

Evaluate the answer professionally.

Give:
- strengths
- weaknesses
- short improvement advice

Keep it concise.
"""
                },

                {
                    "role": "user",

                    "content": f"""
Question:
{question}

Answer:
{answer}
"""
                }
            ]
        )

        feedback = (
            response
            .choices[0]
            .message
            .content
        )

        return jsonify({
            "feedback": feedback
        })

    except Exception as e:

        return jsonify({
            "feedback": str(e)
        })


# =========================
# START APP
# =========================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(
        host="0.0.0.0",
        port=5000
    )
