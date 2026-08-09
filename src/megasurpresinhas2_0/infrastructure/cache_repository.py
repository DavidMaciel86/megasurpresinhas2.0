import json
import os
from pathlib import Path


class JsonCacheRepository:
    def __init__(self, directory: Path) -> None:
        self._directory = directory

    def load(self, lottery_code: str) -> list[int] | None:
        path = self._path(lottery_code)
        if not path.exists():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            numbers = payload.get("numbers")
            return [int(number) for number in numbers] if isinstance(numbers, list) else None
        except (OSError, ValueError, TypeError):
            return None

    def save(self, lottery_code: str, contest: int, numbers: list[int]) -> None:
        self._directory.mkdir(parents=True, exist_ok=True)
        path = self._path(lottery_code)
        temporary = path.with_suffix(".tmp")
        payload = {"lottery": lottery_code, "contest": contest, "numbers": numbers}
        temporary.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        os.replace(temporary, path)

    def _path(self, lottery_code: str) -> Path:
        return self._directory / f"{lottery_code}.json"
