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
# LEARNING RECOMMENDATIONS
# =========================================

def recommend_learning_path(

    skills,

    experience_level
):

    prompt = f"""

Create a professional learning roadmap.

Current skills:
{skills}

Experience level:
{experience_level}

Provide:
- Learning path
- Technologies
- Certifications
- Practice projects
- Career advice

"""

    response = (
        client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",

                    "content": """
You are a senior DevOps mentor.
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
# TOOL RECOMMENDATIONS
# =========================================

def recommend_tools(
    user_goal
):

    prompt = f"""

Recommend the best tools for:

{user_goal}

Include:
- DevOps tools
- AI tools
- Automation tools
- Cloud services
- Productivity tools

"""

    response = (
        client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",

                    "content": """
You are a senior cloud architect.
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
# CAREER RECOMMENDATIONS
# =========================================

def recommend_career(
    profile_description
):

    prompt = f"""

Analyze this user profile and recommend:

- Best IT career paths
- Certifications
- Skills to improve
- Future technologies
- Job opportunities

Profile:

{profile_description}

"""

    response = (
        client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",

                    "content": """
You are a professional IT career advisor.
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
