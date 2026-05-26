import os

import openai

from dotenv import load_dotenv

from models.chat import ChatHistory



# =========================================
# LOAD ENV
# =========================================

load_dotenv()



# =========================================
# OPENAI CLIENT
# =========================================

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)



# =========================================
# AI SYSTEM PROMPTS
# =========================================

AI_MODES = {

    "general": """

You are an advanced AI assistant.

Help professionally and clearly.

""",



    "devops": """

You are a professional DevOps engineer.

Help with:
- Linux
- AWS
- Docker
- Kubernetes
- Networking
- Security
- Terraform
- CI/CD

""",



    "coding": """

You are an expert programming assistant.

Help with:
- Python
- Flask
- JavaScript
- Debugging
- APIs
- Databases
- Automation

""",



    "language": """

You are a professional language assistant.

Help with:
- Translation
- Grammar correction
- Professional emails
- CV optimization
- Writing improvement

""",



    "interview": """

You are a professional technical interviewer.

Ask one question at a time.

Evaluate answers professionally.

""",



    "quiz": """

You are a professional IT quiz generator.

Generate:
- Multiple choice questions
- Correct answers
- Difficulty levels

"""
}



# =========================================
# BUILD MEMORY
# =========================================

def build_memory(
    user_id
):

    previous_chats = (

        ChatHistory.query
        .filter_by(user_id=user_id)
        .order_by(ChatHistory.id.desc())
        .limit(10)
        .all()
    )


    memory_context = ""


    for chat in reversed(previous_chats):

        memory_context += f"""

User:
{chat.user_message}

AI:
{chat.ai_response}

"""

    return memory_context



# =========================================
# GENERATE AI RESPONSE
# =========================================

def generate_ai_response(

    user_id,

    user_message,

    ai_mode="general"
):

    memory_context = build_memory(
        user_id
    )


    system_prompt = (
        AI_MODES.get(
            ai_mode,
            AI_MODES["general"]
        )
    )


    response = (
        client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",

                    "content": f"""

{system_prompt}

Previous conversation memory:

{memory_context}

"""
                },

                {
                    "role": "user",

                    "content": user_message
                }
            ]
        )
    )


    ai_response = (

        response
        .choices[0]
        .message
        .content
    )


    return ai_response
