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
# CODING ASSISTANT
# =========================================

def coding_assistant(

    prompt,

    language="python"
):

    system_prompt = f"""

You are an expert software engineer.

Help professionally with:

- Python
- Flask
- JavaScript
- SQL
- Docker
- Kubernetes
- Terraform
- Linux
- APIs
- Debugging
- Automation

Programming language:
{language}

Always:
- Explain clearly
- Write clean code
- Add comments
- Follow best practices

"""


    response = (
        client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",

                    "content": system_prompt
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
# GENERATE DOCKER COMPOSE
# =========================================

def generate_docker_compose(
    app_description
):

    prompt = f"""

Generate a professional docker-compose.yml
for this project:

{app_description}

"""

    return coding_assistant(

        prompt,

        language="yaml"
    )



# =========================================
# GENERATE TERRAFORM
# =========================================

def generate_terraform(
    infrastructure_description
):

    prompt = f"""

Generate Terraform configuration
for:

{infrastructure_description}

"""

    return coding_assistant(

        prompt,

        language="terraform"
    )



# =========================================
# GENERATE BASH SCRIPT
# =========================================

def generate_bash_script(
    task_description
):

    prompt = f"""

Generate a Bash automation script
for:

{task_description}

"""

    return coding_assistant(

        prompt,

        language="bash"
    )
