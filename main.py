import json
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response, JSONResponse, RedirectResponse

app = FastAPI()

# Q1
@app.get("/hello")
def say_hello():
    with open("hello.html", "r", encoding="utf-8") as file:
        html_content=file.read()
    return Response(content=html_content,status_code=200,media_type="text/html")

# Q2
@app.get("/welcome")
def welcome_user(name:str):
    return Response(content=json.dumps({"message":f"Welcome {name}"}),status_code=200,media_type="application/json")

class Player(BaseModel):
    Number : int
    Name : str

player_list : List[Player] = []

def serialized_player_list():
    converted_player_list = []
    for player in player_list:
        converted_player_list.append(player.model_dump())
    return converted_player_list


# Q3
@app.post("/players")
def post_players(new_player_list : List[Player]):
    for new_player in new_player_list:
        player_list.append(new_player)
    return Response(content=json.dumps({"players":serialized_player_list()}),status_code=201,media_type="application/json")

# Q4
@app.get("/players")
def get_player_list():
    return Response(content=json.dumps({"players" : serialized_player_list()}),status_code=200,media_type="application/json")

# Q5
@app.put("/players")
def modify_player(modified_player_list: List[Player]):
    for modified_player in modified_player_list:
        found = False
        for i,old_player in enumerate(player_list):
            if old_player.Number == modified_player.Number:
                player_list[i] = modified_player
                found = True
                break
        if found is False:
            player_list.append(modified_player)
    return Response(content=json.dumps({"players": serialized_player_list()}),status_code=200,media_type="application/json")

# Q6


# BONUS
@app.get("/players-authorized")
def get_player_list(request : Request):

    return Response(content=json.dumps({"players" : serialized_player_list()}),status_code=200,media_type="application/json")
