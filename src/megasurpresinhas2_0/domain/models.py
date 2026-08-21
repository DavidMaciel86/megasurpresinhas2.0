from dataclasses import dataclass
from enum import StrEnum

from .exceptions import ValidationError


class LotteryCode(StrEnum):
    MEGA_SENA = "megasena"
    LOTOFACIL = "lotofacil"


@dataclass(frozen=True, slots=True)
class LotteryRules:
    code: LotteryCode
    display_name: str
    number_min: int
    number_max: int
    picks_min: int
    picks_max: int
    games_min: int
    games_max: int
    recent_draws: int

    def validate(self, games: int, picks: int) -> None:
        if not self.games_min <= games <= self.games_max:
            raise ValidationError(f"Quantidade de jogos deve estar entre {self.games_min} e {self.games_max}.")
        if not self.picks_min <= picks <= self.picks_max:
            raise ValidationError(f"Quantidade de dezenas deve estar entre {self.picks_min} e {self.picks_max}.")


LOTTERIES = {
    LotteryCode.MEGA_SENA: LotteryRules(LotteryCode.MEGA_SENA, "Mega-Sena", 1, 60, 6, 12, 1, 12, 10),
    LotteryCode.LOTOFACIL: LotteryRules(LotteryCode.LOTOFACIL, "Lotofácil", 1, 25, 15, 20, 1, 1, 3),
}


@dataclass(frozen=True, slots=True)
class GenerationResult:
    games: list[list[int]]
    mode: str
    source: str
    message: str
