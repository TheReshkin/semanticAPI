from pydantic import BaseModel
from typing import Union, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from uuid import uuid4
from bson import ObjectId

from db import db_connect
from db.db_connect import users_collection
from db.db_connect import exercises_collection


class Exercise(BaseModel):
    secret_word: str
    step: int
    username: str
    success: Optional[bool] = False


class User(BaseModel):
    username: str
    token: str
    exercise: str


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


async def find_user_stats(token: str):
    _user = db_connect.find_collection(users_collection, {'token': token})
    return _user['username'], _user['score'], _user['exercise_number']


async def find_exercise(exercise_num):
    _exercise = db_connect.find_collection(exercises_collection, {'_id': ObjectId(exercise_num)})
    if _exercise is not None:
        return _exercise
    else:
        return "No such exercise"


async def find_ex_creator(exercise_num: str):
    _exercise = db_connect.find_collection(exercises_collection, {'_id': ObjectId(exercise_num)})
    if _exercise is not None:
        return _exercise["username"]
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


async def add_step(ex_number: str):
    _exercise = db_connect.find_collection(exercises_collection, {'_id': ObjectId(ex_number)})
    if _exercise is not None:
        step = _exercise["step"] + 1
        db_connect.update_collection(exercises_collection, {"_id": ObjectId(ex_number)}, {"step": step})
        return step
    else:
        return "No such exercise"


async def solve_exercise(ex_number):
    db_connect.update_collection(exercises_collection, {'_id': ObjectId(ex_number)}, {'status': True})
    _exercise = db_connect.find_collection(exercises_collection, {'_id': ObjectId(ex_number)})
    if _exercise is not None:
        username = _exercise["username"]
        _user = db_connect.find_collection(users_collection, {'username': username})
        score = _user["score"] + 1
        db_connect.update_collection(users_collection, {'username': username}, {"score": score})
        return "Ok"
    else:
        return "No such exercise"


async def find_step(ex_number):
    _exercise = db_connect.find_collection(exercises_collection, {'_id': ObjectId(ex_number)})
    if _exercise is not None:
        return _exercise["step"]
    else:
        return "No such exercise"


async def user_set_exercise(user_token, ex_number: str):
    db_connect.update_collection(users_collection, {'token': user_token}, {'exercise_number': ObjectId(ex_number)})
