from flask import (
    Blueprint,
    request,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import (
    secure_filename
)

from database.db import db

from models.document import Document

import os



# =========================================
# BLUEPRINT
# =========================================

upload_routes = Blueprint(
    "upload_routes",
    __name__
)



# =========================================
# ALLOWED FILES
# =========================================

ALLOWED_EXTENSIONS = {

    "pdf",

    "docx",

    "txt"
}



# =========================================
# CHECK FILE TYPE
# =========================================

def allowed_file(
    filename
):

    return (

        "." in filename

        and

        filename.rsplit(
            ".",
            1
        )[1].lower()

        in

        ALLOWED_EXTENSIONS
    )



# =========================================
# UPLOAD DOCUMENT
# =========================================

@upload_routes.route(
    "/upload-document",
    methods=["POST"]
)
@login_required
def upload_document():

    if "document" not in request.files:

        return jsonify({

            "error":
            "No file uploaded"
        })


    file = request.files["document"]


    if file.filename == "":

        return jsonify({

            "error":
            "No selected file"
        })


    if file and allowed_file(
        file.filename
    ):

        filename = secure_filename(
            file.filename
        )

        upload_folder = (
            "static/uploads"
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        file_path = os.path.join(

            upload_folder,

            filename
        )

        file.save(file_path)



        # =========================================
        # SAVE TO DATABASE
        # =========================================

        document = Document(

            user_id=current_user.id,

            filename=filename,

            original_filename=(
                file.filename
            ),

            file_type=(
                filename.split(".")[-1]
            ),

            processed=False
        )


        db.session.add(document)

        current_user.total_documents += 1

        db.session.commit()


        return jsonify({

            "message":
            "Document uploaded successfully.",

            "filename":
            filename
        })


    return jsonify({

        "error":
        "Unsupported file type"
    })



# =========================================
# USER DOCUMENTS
# =========================================

@upload_routes.route(
    "/my-documents"
)
@login_required
def my_documents():

    documents = (

        Document.query
        .filter_by(
            user_id=current_user.id
        )
        .order_by(
            Document.id.desc()
        )
        .all()
    )


    results = []


    for doc in documents:

        results.append({

            "id": doc.id,

            "filename": (
                doc.original_filename
            ),

            "file_type": (
                doc.file_type
            ),

            "processed": (
                doc.processed
            ),

            "summary": (
                doc.ai_summary
            )
        })


    return jsonify(results)
