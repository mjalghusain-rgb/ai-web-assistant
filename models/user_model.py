from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()



class User(
    UserMixin,
    db.Model
):

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
        db.String(200),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(300),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )



    # PROFILE

    bio = db.Column(
        db.Text,
        default=""
    )

    job_title = db.Column(
        db.String(200),
        default=""
    )

    skills = db.Column(
        db.Text,
        default=""
    )

    country = db.Column(
        db.String(100),
        default=""
    )

    experience_level = db.Column(
        db.String(100),
        default=""
    )



    # PROFILE IMAGE

    profile_image = db.Column(
        db.String(300),
        default="default.png"
    )



    # SETTINGS

    dark_mode = db.Column(
        db.Boolean,
        default=True
    )

    voice_enabled = db.Column(
        db.Boolean,
        default=True
    )



    def __repr__(self):

        return f"<User {self.username}>"
