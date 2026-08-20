import logging

from megasurpresinhas2_0.domain.exceptions import ExternalServiceError
from megasurpresinhas2_0.domain.generator import WeightedGameGenerator
from megasurpresinhas2_0.domain.models import LOTTERIES, GenerationResult

from .dto import GenerateGamesRequest
from .ports import CacheRepository, ResultProvider


class GenerationService:
    """
    Orquestra o caso de uso de geração de jogos.

    Coordena a obtenção dos dados históricos, o uso de cache como contingência
    e a geração dos jogos conforme as regras da loteria selecionada.
    """
    
    def __init__(self, provider: ResultProvider, cache: CacheRepository, generator: WeightedGameGenerator, logger=None) -> None:
        self._provider = provider
        self._cache = cache
        self._generator = generator
        self._logger = logger or logging.getLogger(__name__)

    def execute(self, request: GenerateGamesRequest) -> GenerationResult:
        """
        Executa a geração de jogos a partir dos parâmetros da requisição.
    
        Retorna o resultado com os jogos gerados e informações sobre a origem
        dos dados utilizados na geração.
        """
        
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
