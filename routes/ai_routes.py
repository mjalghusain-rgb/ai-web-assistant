from openai import OpenAI
import os
from flask import (
    Blueprint,
    request,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from database.db import db

from models.chat import ChatHistory

from ai.chatbot import (
    generate_ai_response
)

from ai.voice import (
    transcribe_audio
)

from ai.coding import (
    coding_assistant,
    generate_docker_compose,
    generate_terraform,
    generate_bash_script
)

from ai.language_tools import (
    translate_text,
    correct_grammar,
    generate_email,
    optimize_cv
)

from ai.recommendations import (
    recommend_learning_path,
    recommend_tools,
    recommend_career
)

from ai.image_generator import (
    generate_logo,
    generate_avatar,
    generate_devops_diagram
)

import os



# =========================================
# BLUEPRINT
# =========================================
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
ai_routes = Blueprint(
    "ai_routes",
    __name__
)



# =========================================
# MAIN AI CHAT
# =========================================

@ai_routes.route(
    "/chat",
    methods=["POST"]
)
@login_required
def chat():

    data = request.json

    user_message = (
        data.get("message")
    )

    ai_mode = (
        data.get(
            "mode",
            "general"
        )
    )


    ai_response = (
        generate_ai_response(

            current_user.id,

            user_message,

            ai_mode
        )
    )


    chat = ChatHistory(

        user_id=current_user.id,

        user_message=user_message,

        ai_response=ai_response,

        ai_mode=ai_mode
    )


    db.session.add(chat)

    current_user.total_chats += 1

    db.session.commit()


    return jsonify({

        "response": ai_response
    })



# =========================================
# WHISPER TRANSCRIPTION
# =========================================

@ai_routes.route(
    "/transcribe",
    methods=["POST"]
)
@login_required
def transcribe():

    audio_file = request.files["audio"]

    temp_path = (
        "temp_audio.webm"
    )

    audio_file.save(temp_path)


    transcript = (
        transcribe_audio(
            temp_path
        )
    )


    if os.path.exists(temp_path):

        os.remove(temp_path)


    return jsonify({

        "text": transcript
    })



# =========================================
# CODING ASSISTANT
# =========================================

@ai_routes.route(
    "/coding-assistant",
    methods=["POST"]
)
@login_required
def coding_ai():

    data = request.json

    prompt = data.get("prompt")

    language = data.get(
        "language",
        "python"
    )


    response = coding_assistant(

        prompt,

        language
    )


    return jsonify({

        "response": response
    })



# =========================================
# LANGUAGE TOOLS
# =========================================

@ai_routes.route(
    "/translate",
    methods=["POST"]
)
@login_required
def translate():

    data = request.json

    text = data.get("text")

    target_language = data.get(
        "target_language",
        "English"
    )


    response = translate_text(

        text,

        target_language
    )


    return jsonify({

        "response": response
    })



@ai_routes.route(
    "/grammar",
    methods=["POST"]
)
@login_required
def grammar():

    data = request.json

    text = data.get("text")


    response = correct_grammar(
        text
    )


    return jsonify({

        "response": response
    })



# =========================================
# EMAIL GENERATOR
# =========================================

@ai_routes.route(
    "/generate-email",
    methods=["POST"]
)
@login_required
def email_generator():

    data = request.json

    request_text = data.get(
        "request"
    )


    response = generate_email(
        request_text
    )


    return jsonify({

        "response": response
    })



# =========================================
# CV OPTIMIZER
# =========================================

@ai_routes.route(
    "/optimize-cv",
    methods=["POST"]
)
@login_required
def cv_optimizer():

    data = request.json

    cv_text = data.get("cv")


    response = optimize_cv(
        cv_text
    )


    return jsonify({

        "response": response
    })



# =========================================
# LEARNING RECOMMENDATIONS
# =========================================

@ai_routes.route(
    "/learning-path",
    methods=["POST"]
)
@login_required
def learning_path():

    response = recommend_learning_path(

        current_user.skills,

        current_user.experience_level
    )


    return jsonify({

        "response": response
    })



# =========================================
# TOOL RECOMMENDATIONS
# =========================================

@ai_routes.route(
    "/recommend-tools",
    methods=["POST"]
)
@login_required
def tools_recommendation():

    data = request.json

    goal = data.get("goal")


    response = recommend_tools(
        goal
    )


    return jsonify({

        "response": response
    })



# =========================================
# CAREER RECOMMENDATIONS
# =========================================

@ai_routes.route(
    "/career-advice",
    methods=["POST"]
)
@login_required
def career_advice():

    profile = f"""

Skills:
{current_user.skills}

Experience:
{current_user.experience_level}

Job:
{current_user.job_title}

"""


    response = recommend_career(
        profile
    )


    return jsonify({

        "response": response
    })



# =========================================
# IMAGE GENERATION
# =========================================

@ai_routes.route(
    "/generate-logo",
    methods=["POST"]
)
@login_required
def logo_generator():

    data = request.json

    company_name = data.get(
        "company_name"
    )


    image = generate_logo(
        company_name
    )


    return jsonify({

        "image": image
    })



@ai_routes.route(
    "/generate-avatar",
    methods=["POST"]
)
@login_required
def avatar_generator():

    data = request.json

    description = data.get(
        "description"
    )


    image = generate_avatar(
        description
    )


    return jsonify({

        "image": image
    })



@ai_routes.route(
    "/generate-diagram",
    methods=["POST"]
)
@login_required
def diagram_generator():

    data = request.json

    architecture = data.get(
        "architecture"
    )


    image = generate_devops_diagram(
        architecture
    )


    return jsonify({

        "image": image
    })
# =========================================
# IMAGE GENERATION
# =========================================

@ai_routes.route(
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
