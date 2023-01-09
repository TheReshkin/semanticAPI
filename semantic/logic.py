import random
import time
from dataclasses import dataclass
from typing import Optional

import numpy as np

from semantic.dataset import load_word_vectors

from user_data import user


async def _word_similarity(guess: str, target: str) -> float:
    vectors = load_word_vectors()
    v1, v2 = vectors[guess], vectors[target]
    out = np.dot(v1, v2)
    return abs(round(out.item() * 100, 2))


# выбор случайного слово в зависимости от времени
def _choose_random_word(seed: Optional[int] = None) -> str:
    word_bank = list(load_word_vectors().keys())
    if seed is None:
        seed = int(time.time())
    random.seed(seed)
    return random.choice(word_bank)


async def next_guess(token: str, ex_number: str, guess: str):
    exercise = await user.find_exercise(ex_number)
    if exercise != "No such exercise":
        await user.user_set_exercise(token, ex_number)
        try:
            guess_sim = await _word_similarity(guess.lower().strip(), exercise["secret_word"])
        except KeyError:
            return "WORD NOT RECOGNIZED. Please try again."
        # guess_sim = await _word_similarity(guess.lower().strip(), exercise["secret_word"])
        if guess_sim == 100.0:
            step = await user.find_step(ex_number)
            await user.solve_exercise(ex_number)
            return guess_sim, step
        else:
            step = await user.add_step(ex_number)
            return guess_sim, step
    else:
        return "No such exercise"
