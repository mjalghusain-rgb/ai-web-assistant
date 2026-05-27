from datetime import datetime

from models.user_model import db



class Document(
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



    filename = db.Column(

        db.String(300),

        nullable=False
    )



    original_filename = db.Column(

        db.String(300),

        nullable=False
    )



    file_type = db.Column(

        db.String(100),

        default=""
    )



    file_size = db.Column(

        db.Integer,

        default=0
    )



    uploaded_at = db.Column(

        db.DateTime,

        default=datetime.utcnow
    )



    ai_summary = db.Column(

        db.Text,

        default=""
    )



    ai_tags = db.Column(

        db.Text,

        default=""
    )



    def __repr__(self):

        return f"<Document {self.original_filename}>"
