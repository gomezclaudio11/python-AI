from fastapi import FastAPI
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración para la API de GitHub
client = openai.OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN"),
)
MODEL_NAME = os.getenv("GITHUB_MODEL", "gpt-4o")
app = FastAPI()

@app.get("/chat")
def chat(prompt: str):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.7,
        n=1,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"response": response.choices[0].message.content}
