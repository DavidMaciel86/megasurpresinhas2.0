class MegaSurpresinhasError(Exception):
    """Erro conhecido da aplicação."""


class ValidationError(MegaSurpresinhasError):
    """Entrada ou regra de domínio inválida."""


class ExternalServiceError(MegaSurpresinhasError):
    """Falha ao consultar o provedor externo."""


class InvalidApiResponseError(ExternalServiceError):
    """Resposta externa fora do contrato esperado."""
