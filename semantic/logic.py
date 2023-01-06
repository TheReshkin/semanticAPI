import random
import time
from dataclasses import dataclass
from typing import Optional

import numpy as np

from semantic.dataset import load_word_vectors


@dataclass
class SemanticStepInfo:
    guess: str
    similarity: float
    success: bool = False

    def __hash__(self) -> int:
        return hash(f"{self.guess}{self.similarity:.2f}{self.success}")


def _word_similarity(guess: str, target: str) -> float:
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


class Semantic:
    def __init__(self, seed: Optional[int] = None, silent: bool = False):
        self._word = _choose_random_word(seed=seed)
        self.silent = silent

        self._step = 1
        self._success = False

    def _print_step_info(self, info: SemanticStepInfo):
        print(f"Similarity: {info.similarity:.2f}")
        print("\n")
        if info.success:
            print("You win! :)")

    @property
    def done(self):
        return self._success

    def step(self, guess: str) -> SemanticStepInfo:
        similarity = _word_similarity(guess, self._word)
        self._success = guess == self._word
        info = SemanticStepInfo(
            guess=guess, similarity=similarity, success=self._success,
        )

        if not self._success:
            self._step += 1
        if not self.silent:
            self._print_step_info(info)

        return info

    def play(self):
        print("Semantic!\n")

        while not self.done:
            print(f"Step {self._step}")
            guess = input("Enter a guess: ").lower().strip()
            try:
                _ = self.step(guess)
            except KeyError:
                print("\nWORD NOT RECOGNIZED. Please try again.")


def main():
    Semantic().play()


if __name__ == "__main__":
    main()
