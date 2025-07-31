import base64
import json
from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()

# Q1

@app.get("/ping")
def get_ping():
    return Response(content="pong",status_code=200,media_type="text/plain")

# Q2

@app.get("/home")
def get_home():
    with open("welcome.html","r",encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content,status_code=200,media_type="text/html")

# Q4

class PostModel(BaseModel):
    author : str
    title : str
    content : str
    creation_datetime : datetime

stored_posts : List[PostModel] = []

def serialized_stored_posts_isoformat():
    converted_posts = []
    for post in stored_posts:
        post.creation_datetime = post.creation_datetime.isoformat()
        converted_posts.append(post.model_dump())
    return converted_posts

def serialized_stored_posts_format():
    converted_posts = []
    for post in stored_posts:
        converted_posts.append(post.model_dump())
    return converted_posts

@app.post("/posts")
def create_posts(posts_list : List[PostModel]):
    for post in posts_list:
        stored_posts.append(post)
    return Response(
        content=json.dumps(serialized_stored_posts_isoformat()),
        status_code=201,
        media_type="application/json"
    )

# Q5

@app.get("/posts")
def get_posts():
    return Response(
        content=json.dumps(serialized_stored_posts_format()),
        status_code=200,
        media_type="application/json")

# Q6


@app.put("/posts")
def modify_posts(posts_list: List[PostModel]):
    for updated_post in posts_list:
        found = False
        for i,original_post in enumerate(stored_posts):
            if original_post.title == updated_post.title:
                stored_posts[i] = updated_post
                found = True
                break
        if found is False:
            stored_posts.append(updated_post)
    return Response(content=json.dumps(serialized_stored_posts_isoformat()),status_code=200,media_type="application/json")


# BONUS

@app.get("/ping/auth")
def get_ping_auth(request : Request):
    required_value = "admin:123456"
    user_info = request.headers.get("Authorization")
    encoded_user_info = user_info.split(" ")[1]
    decoded_user_info = base64.b64decode(encoded_user_info)
    decoded_user_info_str = decoded_user_info.decode('utf-8')

    if decoded_user_info_str != required_value:
        return Response(content=json.dumps({"message" : "La ressource demandee ne peut pas vous être acceptee"}),status_code=401,media_type="application/json")
    return Response(content="pong",status_code=200,media_type="text/plain")

# Q3

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("not_found.html","r",encoding="utf-8") as file:
        html_content=file.read()
    return Response(content=html_content,status_code=404,media_type="text/html")