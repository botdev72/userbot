import requests

from ubot import OPENAI_KEY

# openai.api_key = random.choice(OPENAI_KEY)

# openai.api_key = OPENAI_KEY

# import openai


class OpenBO:
    @staticmethod
    def ChatGPT(question):
        headers = {
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": question}],
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=data
        )
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"].strip()

    @staticmethod
    def ImageDalle(question):
        headers = {
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "prompt": question,
            "n": 1,
            "size": "1024x1024",
        }

        response = requests.post(
            "https://api.openai.com/v1/images/generations", headers=headers, json=data
        )
        response_data = response.json()
        return response_data["data"][0]["url"]

    @staticmethod
    def SpeechToText(file):
        headers = {
            "Authorization": f"Bearer {OPENAI_KEY}",
        }

        data = {
            "model": "whisper-1",
        }

        with open(file, "rb") as audio:
            files = {"file": audio}

            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers=headers,
                data=data,
                files=files,
            )
            response_data = response.json()
            return response_data["text"]


"""
class OpenAi:
    @staticmethod
    async def ChatGPT(question):
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
        )
        return response.choices[0].message["content"].strip()

    @staticmethod
    async def ImageDalle(question):
        response = await asyncio.to_thread(
            openai.Image.create,
            prompt=question,
            n=1,
        )
        return response["data"][0]["url"]

    @staticmethod
    async def SpeechToText(file):
        audio_file = open(file, "rb")
        response = await asyncio.to_thread(
            openai.Audio.transcribe, "whisper-1", audio_file
        )
        return response["text"]
"""
