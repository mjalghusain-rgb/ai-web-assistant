from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import (
    secure_filename
)

from database.db import db

from models.chat import ChatHistory

import os



# =========================================
# BLUEPRINT
# =========================================

profile_routes = Blueprint(
    "profile_routes",
    __name__
)



# =========================================
# PROFILE PAGE
# =========================================

@profile_routes.route("/profile")
@login_required
def profile():

    saved_chats = (

        ChatHistory.query
        .filter_by(
            user_id=current_user.id
        )
        .order_by(
            ChatHistory.id.desc()
        )
        .limit(10)
        .all()
    )


    return render_template(

        "profile.html",

        user=current_user,

        saved_chats=saved_chats
    )



# =========================================
# UPDATE PROFILE
# =========================================

@profile_routes.route(
    "/update-profile",
    methods=["POST"]
)
@login_required
def update_profile():

    current_user.bio = (
        request.form.get("bio")
    )

    current_user.job_title = (
        request.form.get(
            "job_title"
        )
    )

    current_user.skills = (
        request.form.get("skills")
    )

    current_user.country = (
        request.form.get("country")
    )

    current_user.experience_level = (
        request.form.get(
            "experience_level"
        )
    )



    # =========================================
    # PROFILE IMAGE
    # =========================================

    image = request.files.get(
        "profile_image"
    )

    if image and image.filename != "":

        filename = secure_filename(
            image.filename
        )

        upload_folder = (
            "static/uploads"
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        image_path = os.path.join(

            upload_folder,

            filename
        )

        image.save(image_path)

        current_user.profile_image = (
            filename
        )



    db.session.commit()


    flash(
        "Profile updated successfully."
    )

    return redirect("/profile")



# =========================================
# USER SETTINGS
# =========================================

@profile_routes.route(
    "/toggle-voice"
)
@login_required
def toggle_voice():

    current_user.voice_enabled = (
        not current_user.voice_enabled
    )

    db.session.commit()

    return redirect("/profile")



@profile_routes.route(
    "/toggle-theme"
)
@login_required
def toggle_theme():

    current_user.dark_mode = (
        not current_user.dark_mode
    )

    db.session.commit()

    return redirect("/profile")
