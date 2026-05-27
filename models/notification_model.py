from datetime import datetime

from models.user_model import db



class Notification(
    db.Model
):

    id = db.Column(
        db.Integer,
        primary_key=True
    )



    user_id = db.Column(

        db.Integer,

        db.ForeignKey("user.id"),

        nullable=False
    )



    title = db.Column(

        db.String(200),

        nullable=False
    )



    message = db.Column(

        db.Text,

        nullable=False
    )



    is_read = db.Column(

        db.Boolean,

        default=False
    )



    created_at = db.Column(

        db.DateTime,

        default=datetime.utcnow
    )



    def __repr__(self):

        return f"<Notification {selftitle}>"
