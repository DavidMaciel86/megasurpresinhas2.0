import pytest

from megasurpresinhas2_0.domain.exceptions import ValidationError
from megasurpresinhas2_0.domain.models import LOTTERIES, LotteryCode


def test_mega_sena_aceita_parametros_minimos_validos():
    """Verifica se a Mega-Sena aceita os valores mínimos permitidos pelas regras."""
    rules = LOTTERIES[LotteryCode.MEGA_SENA]

    rules.validate(games=1, picks=6)


def test_mega_sena_aceita_parametros_maximos_validos():
    """Verifica se a Mega-Sena aceita os valores máximos permitidos pelas regras."""
    rules = LOTTERIES[LotteryCode.MEGA_SENA]

    rules.validate(games=12, picks=12)


@pytest.mark.parametrize("games", [0, 13])
def test_mega_sena_rejeita_quantidade_invalida_de_jogos(games):
    """Verifica se a Mega-Sena rejeita quantidades de jogos fora dos limites permitidos."""
    rules = LOTTERIES[LotteryCode.MEGA_SENA]

    with pytest.raises(ValidationError):
        rules.validate(games=games, picks=6)


@pytest.mark.parametrize("picks", [5, 13])
def test_mega_sena_rejeita_quantidade_invalida_de_dezenas(picks):
    """Verifica se a Mega-Sena rejeita quantidades de dezenas fora dos limites permitidos."""
    rules = LOTTERIES[LotteryCode.MEGA_SENA]

    with pytest.raises(ValidationError):
        rules.validate(games=1, picks=picks)


def test_lotofacil_aceita_parametros_minimos_validos():
    """Verifica se a Lotofácil aceita os valores mínimos permitidos pelas regras."""
    rules = LOTTERIES[LotteryCode.LOTOFACIL]

    rules.validate(games=1, picks=15)


def test_lotofacil_aceita_parametros_maximos_validos():
    """Verifica se a Lotofácil aceita os valores máximos permitidos pelas regras."""
    rules = LOTTERIES[LotteryCode.LOTOFACIL]

    rules.validate(games=1, picks=20)


@pytest.mark.parametrize("games", [0, 2])
def test_lotofacil_rejeita_quantidade_invalida_de_jogos(games):
    """Verifica se a Lotofácil rejeita quantidades de jogos fora dos limites permitidos."""
    rules = LOTTERIES[LotteryCode.LOTOFACIL]

    with pytest.raises(ValidationError):
        rules.validate(games=games, picks=15)


@pytest.mark.parametrize("picks", [14, 21])
def test_lotofacil_rejeita_quantidade_invalida_de_dezenas(picks):
    """Verifica se a Lotofácil rejeita quantidades de dezenas fora dos limites permitidos."""
    rules = LOTTERIES[LotteryCode.LOTOFACIL]

    with pytest.raises(ValidationError):
        rules.validate(games=1, picks=picks)
