from fastapi import FastAPI
import semantic.logic
from fastapi import Depends, FastAPI, HTTPException, status

# from fastapi.security import OAuth2PasswordRequestForm
from user_data import user
import semantic
app = FastAPI()


@app.post("/get_token")
async def login(username: str):
    user_token = await user.sign_in(username)
    return {"access_token": user_token}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/start")
async def start_game(token: str, word: str):
    user_name = await user.find_user(token)
    # добавить рандомайзер слов
    ex_number = await user.create_exercise("boy", user_name)
    similarity = await semantic.logic.next_guess(ex_number, word)
    return {"Guess: ": word, "Similarity: ": similarity}


@app.get("/similarity")
async def word_similarity(word: str):
    return {semantic.logic._word_similarity('boy', word)}


@app.get("/next_guess")
async def next_guess(form_data:  user.User = Depends()):
    await semantic.logic.next_guess()
    return {"username": form_data.username, "token": form_data.token, "exercise": form_data.exercise}
