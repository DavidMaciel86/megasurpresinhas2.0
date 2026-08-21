import requests

from megasurpresinhas2_0.domain.exceptions import (
    ExternalServiceError,
    InvalidApiResponseError,
)
from megasurpresinhas2_0.domain.models import LotteryRules


class GuidiLotteryApiClient:
    def __init__(self, base_url: str, timeout: tuple[float, float], session=None) -> None:
        self._base_url = base_url
        self._timeout = timeout
        self._session = session or requests.Session()
        self._session.headers.update({"Accept": "application/json", "User-Agent": "MegaSurpresinhas2/2.0"})

    def recent_numbers(self, rules: LotteryRules) -> tuple[list[int], int]:
        latest = self._get_json(f"{self._base_url}/{rules.code.value}/ultimo")
        try:
            contest = int(latest["numero"])
        except (KeyError, TypeError, ValueError) as exc:
            raise InvalidApiResponseError("Número do concurso ausente ou inválido.") from exc
        numbers: list[int] = []
        for number in range(contest, contest - rules.recent_draws, -1):
            payload = self._get_json(f"{self._base_url}/{rules.code.value}/{number}")
            values = payload.get("listaDezenas")
            if not isinstance(values, list) or not values:
                raise InvalidApiResponseError(f"Dezenas ausentes no concurso {number}.")
            try:
                numbers.extend(int(value) for value in values)
            except (TypeError, ValueError) as exc:
                raise InvalidApiResponseError(f"Dezenas inválidas no concurso {number}.") from exc
        return numbers, contest

    def _get_json(self, url: str) -> dict:
        try:
            response = self._session.get(url, timeout=self._timeout)
            response.raise_for_status()
            payload = response.json()
        except (requests.RequestException, ValueError) as exc:
            raise ExternalServiceError("Falha na consulta à API de loterias.") from exc
        if not isinstance(payload, dict):
            raise InvalidApiResponseError("Formato inesperado na resposta da API.")
        return payload
