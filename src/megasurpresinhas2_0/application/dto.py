from dataclasses import dataclass
from megasurpresinhas2_0.domain.models import LotteryCode


@dataclass(frozen=True, slots=True)
class GenerateGamesRequest:
    lottery: LotteryCode
    games: int
    picks: int
