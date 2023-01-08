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


@app.get("/start_new_game")
async def start_game(token: str, word: str):
    user_name = await user.find_user(token)
    # добавить рандомайзер слов
    ex_number = await user.create_exercise("boy", user_name)
    similarity = await semantic.logic.next_guess(ex_number, word)
    return {"Guess: ": word, "Similarity: ": similarity, "Exercise num:": str(ex_number)}


@app.get("/next_guess")
async def guess_next(token: str, ex_number: str, word: str):
    username = await user.find_user(token)
    ex_creator = await user.find_ex_creator(ex_number)
    print(username, ex_creator)
    if username == ex_creator:
        sim_step = await semantic.logic.next_guess(ex_number, word)
        return {"Guess: ": word, "Similarity: ": sim_step[0], "Step:": sim_step[1], "Exercise num:": str(ex_number)}
    elif ex_creator == "No such exercise":
        return "No such exercise"
    elif username != ex_creator:
        return "You have no access to this exercise"
    else:
        return "Something went wrong"


@app.get("/get_my_stats")
async def stats(token: str):
    response = await user.find_user_stats(token)
    return {"username": response[0], "score": response[1], "ex_number": response[2]}


@app.get("/get_last_exercise")
async def last_exercise(token: str):
    ex_number = ""
    return {"Exercise number: ": ex_number}
