import random
from collections import Counter
from collections.abc import Sequence
from .exceptions import ValidationError
from .models import LotteryRules


class WeightedGameGenerator:
    def __init__(self, rng=None) -> None:
        self._rng = rng or random.SystemRandom()

    def generate(self, rules: LotteryRules, games: int, picks: int, historical_numbers: Sequence[int]) -> list[list[int]]:
        rules.validate(games, picks)
        if any(not rules.number_min <= number <= rules.number_max for number in historical_numbers):
            raise ValidationError("A fonte de dados retornou dezenas fora da faixa permitida.")
        frequencies = Counter(historical_numbers)
        population = list(range(rules.number_min, rules.number_max + 1))
        weights = [frequencies[number] + 1 for number in population]
        return [sorted(self._sample(population, weights, picks)) for _ in range(games)]

    def _sample(self, population: list[int], weights: list[int], size: int) -> list[int]:
        available, current_weights, selected = population.copy(), weights.copy(), []
        for _ in range(size):
            chosen = self._rng.choices(available, weights=current_weights, k=1)[0]
            index = available.index(chosen)
            selected.append(available.pop(index))
            current_weights.pop(index)
        return selected
