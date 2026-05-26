from database.db import db



class ChatHistory(
    db.Model
):

    id = db.Column(
        db.Integer,
        primary_key=True
    )



    # =========================================
    # USER
    # =========================================

    user_id = db.Column(
        db.Integer,
        nullable=False
    )



    # =========================================
    # CHAT CONTENT
    # =========================================

    user_message = db.Column(
        db.Text,
        nullable=False
    )

    ai_response = db.Column(
        db.Text,
        nullable=False
    )



    # =========================================
    # AI MODE
    # =========================================

    ai_mode = db.Column(
        db.String(100),
        default="general"
    )



    # =========================================
    # SAVED CHAT
    # =========================================

    is_saved = db.Column(
        db.Boolean,
        default=False
    )



    # =========================================
    # CREATED DATE
    # =========================================

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
