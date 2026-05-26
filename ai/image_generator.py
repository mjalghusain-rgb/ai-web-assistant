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
# GENERATE IMAGE
# =========================================

def generate_image(
    prompt
):

    response = (
        client.images.generate(

            model="gpt-image-1",

            prompt=prompt,

            size="1024x1024"
        )
    )


    image_base64 = (
        response.data[0].b64_json
    )

    return image_base64



# =========================================
# GENERATE LOGO
# =========================================

def generate_logo(
    company_name
):

    prompt = f"""

Create a modern professional logo for:

{company_name}

Style:
- Modern
- Minimal
- SaaS
- Professional
- Clean

"""

    return generate_image(prompt)



# =========================================
# GENERATE DEVOPS DIAGRAM
# =========================================

def generate_devops_diagram(
    architecture_description
):

    prompt = f"""

Create a professional DevOps architecture diagram for:

{architecture_description}

Include:
- AWS
- Docker
- Kubernetes
- CI/CD
- Networking

Professional technical style.

"""

    return generate_image(prompt)



# =========================================
# GENERATE AVATAR
# =========================================

def generate_avatar(
    description
):

    prompt = f"""

Create a modern AI avatar.

Description:

{description}

Style:
- Professional
- Realistic
- Modern
- Clean

"""

    return generate_image(prompt)
