from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
async def hello():
    env = os.getenv("APP_NAME")
    return { "Name": env }
