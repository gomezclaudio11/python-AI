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


@app.get("/")
def read_root():
    return {"message": "¡Hola! Esta es una API con OpenAI."}

@app.post("/generate/")
def generate_response(prompt: str):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.7,
        max_tokens=100,
        n=1,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )


    async def event_generator():
        for event in response:
            if event.choices and event.choices[0].delta.content:
                yield event.choices[0].delta.content

    return StreamingResponse(event_generator(), media_type="text/plain")

"""
Se usa StreamingResponse

    Permite enviar la respuesta en partes en lugar de esperar a que termine todo.

Se crea event_generator()

    Itera sobre el response en stream=True, extrayendo los fragmentos del texto generado.

Se devuelve StreamingResponse(event_generator())

    Envía la respuesta en tiempo real en formato text/plain.
"""