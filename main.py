from fastapi import FastAPI
import semantic.logic

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/start")
async def start_game():
    return {semantic.logic.main()}


@app.get("/similarity")
async def word_similarity(word: str):
    return {semantic.logic._word_similarity('boy', word)}
