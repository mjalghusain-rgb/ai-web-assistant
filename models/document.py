from database.db import db



class Document(
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
    # FILE INFO
    # =========================================

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    original_filename = db.Column(
        db.String(255),
        nullable=False
    )

    file_type = db.Column(
        db.String(50),
        default="txt"
    )



    # =========================================
    # AI ANALYSIS
    # =========================================

    ai_summary = db.Column(
        db.Text,
        default=""
    )

    extracted_text = db.Column(
        db.Text,
        default=""
    )



    # =========================================
    # STATUS
    # =========================================

    processed = db.Column(
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
