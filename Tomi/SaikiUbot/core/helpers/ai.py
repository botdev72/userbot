import random

import openai

from SaikiUbot.config import OPENAI_KEY


class OpenAi:
    def ChatGPT(question):
        openai.api_key = random.choice(OPENAI_KEY)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0.5,
            stop=None,
            n=1,
            user="arc",
            max_tokens=768,
        )
        return response["choices"][0].text.strip()

    def ImageDalle(question):
        openai.api_key = random.choice(OPENAI_KEY)
        response = openai.Image.create(
            prompt=question,
            n=1,
            size="1024x1024",
            user="arc",
        )
        return response["data"][0]["url"]

    def SpeechToText(out_file):
        openai.api_key = random.choice(OPENAI_KEY)
        audio_file = open(out_file, "rb")
        response = openai.Audio.transcribe("whisper-1", audio_file)
        return response["text"]
