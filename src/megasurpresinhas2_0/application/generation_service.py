import logging
from .dto import GenerateGamesRequest
from .ports import CacheRepository, ResultProvider
from megasurpresinhas2_0.domain.exceptions import ExternalServiceError
from megasurpresinhas2_0.domain.generator import WeightedGameGenerator
from megasurpresinhas2_0.domain.models import GenerationResult, LOTTERIES


class GenerationService:
    def __init__(self, provider: ResultProvider, cache: CacheRepository, generator: WeightedGameGenerator, logger=None) -> None:
        self._provider = provider
        self._cache = cache
        self._generator = generator
        self._logger = logger or logging.getLogger(__name__)

    def execute(self, request: GenerateGamesRequest) -> GenerationResult:
        rules = LOTTERIES[request.lottery]
        rules.validate(request.games, request.picks)
        numbers, mode, source, message = self._resolve_numbers(rules)
        games = self._generator.generate(rules, request.games, request.picks, numbers)
        return GenerationResult(games, mode, source, message)

    def _resolve_numbers(self, rules):
        try:
            numbers, contest = self._provider.recent_numbers(rules)
            try:
                self._cache.save(rules.code.value, contest, numbers)
            except OSError:
                self._logger.warning("Não foi possível atualizar o cache de %s.", rules.code, exc_info=True)
            return numbers, "online", "api", "Dados recentes consultados com sucesso."
        except ExternalServiceError:
            self._logger.warning("API indisponível para %s; tentando cache.", rules.code, exc_info=True)
            cached = self._cache.load(rules.code.value)
            if cached:
                return cached, "cache", "cache", "API indisponível. Usando dados armazenados em cache."
            return [], "fallback", "uniforme", "API e cache indisponíveis. Usando distribuição uniforme."
