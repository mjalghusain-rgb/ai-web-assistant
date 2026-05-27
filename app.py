from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    send_from_directory
)

from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from openai import OpenAI

import os
import uuid



# =========================================
# MODELS
# =========================================

from models.user_model import (
    db,
    User
)

from models.notification_model import (
    Notification
)

from models.document_model import (
    Document
)



# =========================================
# APP
# =========================================

app = Flask(__name__)

app.secret_key = "super-secret-key"



# =========================================
# DATABASE
# =========================================

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///database.db"

app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False

app.config[
    "UPLOAD_FOLDER"
] = "uploads"



db.init_app(app)



# =========================================
# LOGIN MANAGER
# =========================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"



@login_manager.user_loader
def load_user(user_id):

    return User.query.get(
        int(user_id)
    )



# =========================================
# OPENAI
# =========================================

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)



# =========================================
# CREATE DATABASE
# =========================================

with app.app_context():

    db.create_all()



# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    return render_template(
        "home.html"
    )



# =========================================
# DASHBOARD
# =========================================

@app.route("/dashboard")
@login_required
def dashboard():

    notifications = Notification.query.filter_by(

        user_id=current_user.id

    ).order_by(

        Notification.created_at.desc()

    ).limit(5).all()


    documents = Document.query.filter_by(

        user_id=current_user.id

    ).all()


    return render_template(

        "index.html",

        username=current_user.username,

        user=current_user,

        notifications=notifications,

        documents=documents
    )



# =========================================
# REGISTER
# =========================================

@app.route(
    "/register",
    methods=["GET","POST"]
)
def register():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )


        existing_user = User.query.filter(

            (
                User.username == username
            ) |

            (
                User.email == email
            )

        ).first()


        if existing_user:

            return "User already exists"


        hashed_password = generate_password_hash(
            password
        )


        user = User(

            username=username,

            email=email,

            password=hashed_password
        )


        db.session.add(user)

        db.session.commit()


        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )



# =========================================
# LOGIN
# =========================================

@app.route(
    "/login",
    methods=["GET","POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )


        user = User.query.filter_by(
            email=email
        ).first()


        if user and check_password_hash(

            user.password,

            password
        ):

            login_user(user)

            return redirect(
                url_for("dashboard")
            )


        return "Invalid credentials"


    return render_template(
        "login.html"
    )



# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("home")
    )



# =========================================
# CHAT
# =========================================

@app.route(
    "/chat",
    methods=["POST"]
)
@login_required
def chat():

    data = request.get_json()

    user_message = data.get(
        "message"
    )


    system_prompt = """

You are DevOps AI.

You help with:
- DevOps
- Docker
- Kubernetes
- Terraform
- Python
- Linux
- Networking
- AI
- Cloud
- Security

Always format code
inside markdown blocks.

"""


    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role":"system",
                    "content":system_prompt
                },

                {
                    "role":"user",
                    "content":user_message
                }
            ]
        )


        ai_response = response.choices[
            0
        ].message.content


        return jsonify({

            "response":ai_response
        })


    except Exception as e:

        return jsonify({

            "response":f"Error: {str(e)}"
        })



# =========================================
# IMAGE GENERATION
# =========================================

@app.route(
    "/generate-image",
    methods=["POST"]
)
@login_required
def generate_image():

    data = request.get_json()

    prompt = data.get("prompt")


    try:

        response = client.images.generate(

            model="gpt-image-1",

            prompt=prompt,

            size="1024x1024"
        )


        image_url = (
            response.data[0].url
        )


        return jsonify({

            "image_url": image_url
        })


    except Exception as e:

        return jsonify({

            "error": str(e)
        }),500



# =========================================
# DOCUMENT UPLOAD
# =========================================

@app.route(
    "/upload-document",
    methods=["POST"]
)
@login_required
def upload_document():

    if "document" not in request.files:

        return jsonify({

            "error":"No file"
        })


    file = request.files[
        "document"
    ]


    filename = secure_filename(
        file.filename
    )

    unique_name = f"{uuid.uuid4()}_{filename}"

    save_path = os.path.join(

        app.config["UPLOAD_FOLDER"],

        unique_name
    )


    os.makedirs(

        app.config["UPLOAD_FOLDER"],

        exist_ok=True
    )


    file.save(save_path)


    document = Document(

        user_id=current_user.id,

        filename=unique_name,

        original_filename=filename,

        file_type=file.content_type,

        file_size=os.path.getsize(
            save_path
        )
    )


    db.session.add(document)

    db.session.commit()


    notification = Notification(

        user_id=current_user.id,

        title="Document Uploaded",

        message=f"{filename} uploaded successfully"
    )


    db.session.add(notification)

    db.session.commit()


    return jsonify({

        "filename":filename
    })



# =========================================
# PROFILE
# =========================================

@app.route(
    "/profile",
    methods=["GET","POST"]
)
@login_required
def profile():

    if request.method == "POST":


        # PROFILE IMAGE

        if "profile_image" in request.files:

            image = request.files[
                "profile_image"
            ]


            if image.filename != "":

                filename = secure_filename(
                    image.filename
                )

                unique_name = f"{uuid.uuid4()}_{filename}"

                save_path = os.path.join(

                    app.config["UPLOAD_FOLDER"],

                    unique_name
                )

                image.save(save_path)

                current_user.profile_image = unique_name



        current_user.username = request.form.get(
            "username"
        )

        current_user.email = request.form.get(
            "email"
        )

        current_user.job_title = request.form.get(
            "job_title"
        )

        current_user.country = request.form.get(
            "country"
        )

        current_user.experience_level = request.form.get(
            "experience_level"
        )

        current_user.bio = request.form.get(
            "bio"
        )

        current_user.skills = request.form.get(
            "skills"
        )


        db.session.commit()


        notification = Notification(

            user_id=current_user.id,

            title="Profile Updated",

            message="Your profile was updated successfully"
        )


        db.session.add(notification)

        db.session.commit()


    return render_template(

        "profile.html",

        user=current_user
    )



# =========================================
# DOCUMENTS PAGE
# =========================================

@app.route("/documents")
@login_required
def documents_page():

    documents = Document.query.filter_by(

        user_id=current_user.id

    ).order_by(

        Document.uploaded_at.desc()

    ).all()


    return render_template(

        "documents.html",

        documents=documents
    )



# =========================================
# TOOLS PAGE
# =========================================

@app.route("/tools")
@login_required
def tools_page():

    return render_template(
        "tools.html"
    )



# =========================================
# AGENTS PAGE
# =========================================

@app.route("/agents")
@login_required
def agents_page():

    return render_template(
        "agents.html"
    )



# =========================================
# ROADMAP PAGE
# =========================================

@app.route("/roadmap")
@login_required
def roadmap_page():

    return render_template(
        "roadmap.html"
    )



# =========================================
# NOTIFICATIONS API
# =========================================

@app.route("/notifications")
@login_required
def get_notifications():

    notifications = Notification.query.filter_by(

        user_id=current_user.id

    ).order_by(

        Notification.created_at.desc()

    ).all()


    result = []


    for n in notifications:

        result.append({

            "title":n.title,

            "message":n.message
        })


    return jsonify(result)



# =========================================
# UPLOADS
# =========================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(

        app.config["UPLOAD_FOLDER"],

        filename
    )



# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True
    )
