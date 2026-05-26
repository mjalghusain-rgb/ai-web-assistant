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
# TRANSCRIBE AUDIO
# =========================================

def transcribe_audio(
    audio_path
):

    with open(
        audio_path,
        "rb"
    ) as audio_file:

        transcript = (
            client.audio.transcriptions.create(

                model="whisper-1",

                file=audio_file
            )
        )

    return transcript.text
