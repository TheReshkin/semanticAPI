from pydantic import BaseModel
from typing import Union, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from uuid import uuid4

from db import db_connect
from db.db_connect import users_collection
from db.db_connect import exercises_collection

users = {
    "pupochek": {
        "username": "pupochek",
        "token": "pupochek",
        "exercise_number": 1
    }
}
exercises = {
    "1": {
        "exercise_num": 1,
        "secret_word": "human",
        "step": 0,
        "username": "pupkin",
        "status": False
    }
}


class Exercise(BaseModel):
    secret_word: str
    step: int
    username: str
    success: Optional[bool] = False


class User(BaseModel):
    username: str
    token: str
    exercise: int


async def sign_in(username: str):
    _user = db_connect.find_collection(users_collection, {'username': username})
    if _user is None:
        token_rnd = uuid4()
        user = {
            "username": username,
            "token": str(token_rnd),
            "exercise_number": None,
            "score": 0
        }
        db_connect.insert_collection(users_collection, user)
        return token_rnd
    else:
        return _user["token"]


async def find_user(token: str):
    _user = db_connect.find_collection(users_collection, {'token': token})
    return _user['username']


async def find_exercise(exercise_num):
    _exercise = db_connect.find_collection(exercises_collection, {'_id': exercise_num})
    if _exercise is not None:
        return _exercise
    else:
        return "No such exercise"


async def create_exercise(secret_word: str, username: str):
    data = {
        "secret_word": secret_word,
        "step": 0,
        "username": username,
        "status": False
    }
    return db_connect.insert_collection(exercises_collection, data)


async def add_step(exercise_num: str):
    _exercise = db_connect.find_collection(exercises_collection, {'_id': exercise_num})
    if _exercise is not None:
        step = _exercise["step"] + 1
        db_connect.update_document(exercises_collection, {"_id": exercise_num}, {"step": step})
    else:
        return "No such exercise"
