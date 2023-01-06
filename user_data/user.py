from pydantic import BaseModel
from typing import Union, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="sign_in")

users = {
    "pupochek": {
        "username": "pupochek",
        "token": "pupochek",
        "exercise_number": 1
    }
}
exercises = {
    "1": {
        "secret_word": "human",
        "step": 0,
        "exercise_number": 1
    }
}


class Exercise(BaseModel):
    secret_word: str
    step: int
    exercise_number: Optional[int] = None


class User(BaseModel):
    username: str
    token: str
    exercise: int
