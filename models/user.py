from flask_login import UserMixin

from database.db import db



class User(
    UserMixin,
    db.Model
):

    id = db.Column(
        db.Integer,
        primary_key=True
    )



    # =========================================
    # AUTH
    # =========================================

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



    # =========================================
    # ROLES
    # =========================================

    is_admin = db.Column(
        db.Boolean,
        default=False
    )



    # =========================================
    # PROFILE
    # =========================================

    bio = db.Column(
        db.Text,
        default=""
    )

    job_title = db.Column(
        db.String(120),
        default=""
    )

    skills = db.Column(
        db.Text,
        default=""
    )

    country = db.Column(
        db.String(120),
        default=""
    )

    experience_level = db.Column(
        db.String(120),
        default=""
    )

    profile_image = db.Column(
        db.String(255),
        default="default.png"
    )



    # =========================================
    # SETTINGS
    # =========================================

    voice_enabled = db.Column(
        db.Boolean,
        default=True
    )

    dark_mode = db.Column(
        db.Boolean,
        default=True
    )



    # =========================================
    # USER STATS
    # =========================================

    total_chats = db.Column(
        db.Integer,
        default=0
    )

    total_documents = db.Column(
        db.Integer,
        default=0
    )

    total_generated_cvs = db.Column(
        db.Integer,
        default=0
    )



    # =========================================
    # CREATED DATE
    # =========================================

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
