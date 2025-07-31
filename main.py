import json

from fastapi import FastAPI
from starlette.responses import Response

app = FastAPI()

# Q1

@app.get("/ping")
def get_ping():
    return Response(content="pong",status_code=200)

# Q2

@app.get("/home")
def get_home():
    with open("welcome.html","r",encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content,status_code=200,media_type="text/html")

# Q3


@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("not_found.html","r",encoding="utf-8") as file:
        html_content=file.read()
    return Response(content=html_content,status_code=404,media_type="text/html")