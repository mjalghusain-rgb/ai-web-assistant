import os

import openai

from dotenv import load_dotenv



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
# TRANSLATION
# =========================================

def translate_text(

    text,

    target_language="English"
):

    prompt = f"""

Translate the following text to
{target_language}.

Keep the meaning accurate.

Text:
{text}

"""


    response = (
        client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",

                    "content": """
You are a professional translator.
"""
                },

                {
                    "role": "user",

                    "content": prompt
                }
            ]
        )
    )


    return (

        response
        .choices[0]
        .message
        .content
    )



# =========================================
# GRAMMAR CORRECTION
# =========================================

def correct_grammar(
    text
):

    prompt = f"""

Correct grammar and improve clarity
for this text:

{text}

"""


    response = (
        client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",

                    "content": """
You are a professional English editor.
"""
                },

                {
                    "role": "user",

                    "content": prompt
                }
            ]
        )
    )


    return (

        response
        .choices[0]
        .message
        .content
    )



# =========================================
# PROFESSIONAL EMAIL
# =========================================

def generate_email(
    email_request
):

    prompt = f"""

Write a professional email for:

{email_request}

"""


    response = (
        client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",

                    "content": """
You are a professional business writer.
"""
                },

                {
                    "role": "user",

                    "content": prompt
                }
            ]
        )
    )


    return (

        response
        .choices[0]
        .message
        .content
    )



# =========================================
# CV OPTIMIZATION
# =========================================

def optimize_cv(
    cv_text
):

    prompt = f"""

Optimize this CV professionally.

Improve:
- ATS compatibility
- Formatting
- Wording
- Skills presentation

CV:

{cv_text}

"""


    response = (
        client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",

                    "content": """
You are an expert HR recruiter.
"""
                },

                {
                    "role": "user",

                    "content": prompt
                }
            ]
        )
    )


    return (

        response
        .choices[0]
        .message
        .content
    )
