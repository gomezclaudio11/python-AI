from fastapi import FastAPI
import openai
import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
load_dotenv()

# Configuración para la API de GitHub
client = openai.OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN"),
)
MODEL_NAME = os.getenv("GITHUB_MODEL", "gpt-4o")
app = FastAPI()

messages = [
    {"role": "system", "content": "I am a teaching assistant helping with Python questions for Berkeley CS 61A."},
]

while True:
    question = input("\nYour question: ")
    print("Sending question...")

    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=1,
        max_tokens=400,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    bot_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": bot_response})

    print("Answer: ")
    print(bot_response)
