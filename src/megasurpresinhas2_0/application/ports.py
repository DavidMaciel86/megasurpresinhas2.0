from typing import Protocol

from megasurpresinhas2_0.domain.models import LotteryRules


class ResultProvider(Protocol):
    def recent_numbers(self, rules: LotteryRules) -> tuple[list[int], int]: ...


class CacheRepository(Protocol):
    def load(self, lottery_code: str) -> list[int] | None: ...
    def save(self, lottery_code: str, contest: int, numbers: list[int]) -> None: ...
