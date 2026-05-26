from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    flash,
    send_file
)

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

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

import openai
import os
import re



# ==================================================
# LOAD ENV
# ==================================================

load_dotenv()



# ==================================================
# FLASK CONFIG
# ==================================================

app = Flask(__name__)

app.secret_key = "supersecretkey_v2"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///users.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



# ==================================================
# LOGIN MANAGER
# ==================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"



# ==================================================
# OPENAI CLIENT
# ==================================================

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)



# ==================================================
# USER MODEL
# ==================================================

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
        db.String(255),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )



# ==================================================
# CHAT HISTORY MODEL
# ==================================================

class ChatHistory(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    user_message = db.Column(
        db.Text,
        nullable=False
    )

    ai_response = db.Column(
        db.Text,
        nullable=False
    )



# ==================================================
# LOGIN LOADER
# ==================================================

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(
        int(user_id)
    )



# ==================================================
# PASSWORD VALIDATION
# ==================================================

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



# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
@login_required
def home():

    return render_template(
        "index.html",
        username=current_user.username
    )



# ==================================================
# ADMIN DASHBOARD
# ==================================================

@app.route("/admin")
@login_required
def admin_dashboard():

    if not current_user.is_admin:

        return "Access denied"

    total_users = User.query.count()

    total_chats = ChatHistory.query.count()

    latest_users = (
        User.query
        .order_by(User.id.desc())
        .limit(5)
        .all()
    )

    return render_template(

        "admin.html",

        total_users=total_users,

        total_chats=total_chats,

        latest_users=latest_users
    )



# ==================================================
# REGISTER
# ==================================================

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



# ==================================================
# LOGIN
# ==================================================

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


        flash(
            "Invalid email or password."
        )


    return render_template(
        "login.html"
    )



# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")



# ==================================================
# CHAT API
# ==================================================

@app.route("/chat", methods=["POST"])
@login_required
def chat():

    data = request.json

    user_message = data["message"]


    previous_chats = (
        ChatHistory.query
        .filter_by(user_id=current_user.id)
        .order_by(ChatHistory.id.desc())
        .limit(5)
        .all()
    )


    memory_context = ""


    for chat_item in reversed(previous_chats):

        memory_context += f"""

User:
{chat_item.user_message}

AI:
{chat_item.ai_response}

"""


    try:

        response = (
            client.chat.completions.create(

                model="gpt-3.5-turbo",

                messages=[

                    {
                        "role": "system",

                        "content": f"""
You are an advanced AI DevOps assistant.

Current user:
{current_user.username}

You remember previous conversations.

Previous memory:
{memory_context}

Help professionally with:
- Linux
- AWS
- Docker
- Networking
- Security
- DevOps
"""
                    },

                    {
                        "role": "user",

                        "content": user_message
                    }
                ]
            )
        )


        ai_response = (
            response
            .choices[0]
            .message
            .content
        )


        new_chat = ChatHistory(

            user_id=current_user.id,

            user_message=user_message,

            ai_response=ai_response
        )


        db.session.add(new_chat)

        db.session.commit()


        return jsonify({

            "response": ai_response
        })


    except Exception as e:

        return jsonify({

            "response": str(e)
        })



# ==================================================
# WHISPER TRANSCRIPTION
# ==================================================

@app.route("/transcribe", methods=["POST"])
@login_required
def transcribe():

    try:

        audio_file = request.files["audio"]


        with open(
            "temp_audio.webm",
            "wb"
        ) as f:

            f.write(
                audio_file.read()
            )


        with open(
            "temp_audio.webm",
            "rb"
        ) as audio:

            transcript = (
                client.audio.transcriptions.create(

                    model="whisper-1",

                    file=audio
                )
            )


        return jsonify({

            "text": transcript.text
        })


    except Exception as e:

        return jsonify({

            "text": str(e)
        })



# ==================================================
# PDF CV GENERATOR
# ==================================================

@app.route(
    "/generate-cv-pdf",
    methods=["POST"]
)
@login_required
def generate_cv_pdf():

    data = request.json

    cv_text = data["cv_text"]


    pdf_file = "generated_cv.pdf"


    doc = SimpleDocTemplate(
        pdf_file
    )

    styles = getSampleStyleSheet()

    elements = []


    elements.append(

        Paragraph(

            cv_text.replace(
                "\n",
                "<br/>"
            ),

            styles["BodyText"]
        )
    )


    elements.append(
        Spacer(1, 12)
    )


    doc.build(elements)


    return send_file(

        pdf_file,

        as_attachment=True
    )



# ==================================================
# START APP
# ==================================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()


    app.run(

        host="0.0.0.0",

        port=5000
    )
