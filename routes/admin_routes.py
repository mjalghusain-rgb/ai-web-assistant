from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required,
    current_user
)

from models.user import User

from models.chat import ChatHistory

from models.document import Document



# =========================================
# BLUEPRINT
# =========================================

admin_routes = Blueprint(
    "admin_routes",
    __name__
)



# =========================================
# ADMIN DASHBOARD
# =========================================

@admin_routes.route("/admin")
@login_required
def admin_dashboard():

    if not current_user.is_admin:

        return "Access denied"



    # =========================================
    # STATS
    # =========================================

    total_users = (
        User.query.count()
    )

    total_chats = (
        ChatHistory.query.count()
    )

    total_documents = (
        Document.query.count()
    )



    # =========================================
    # RECENT USERS
    # =========================================

    latest_users = (

        User.query
        .order_by(User.id.desc())
        .limit(10)
        .all()
    )



    # =========================================
    # RECENT CHATS
    # =========================================

    recent_chats = (

        ChatHistory.query
        .order_by(ChatHistory.id.desc())
        .limit(10)
        .all()
    )



    return render_template(

        "admin.html",

        total_users=total_users,

        total_chats=total_chats,

        total_documents=total_documents,

        latest_users=latest_users,

        recent_chats=recent_chats
    )
