import pytest

from megasurpresinhas2_0.application.dto import GenerateGamesRequest
from megasurpresinhas2_0.domain.exceptions import ExternalServiceError
from megasurpresinhas2_0.domain.models import GenerationResult, LotteryCode


def test_megasena_page_returns_200(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Mega-Sena" in response.get_data(as_text=True)


def test_lotofacil_page_returns_200(client):
    response = client.get("/lotofacil")

    assert response.status_code == 200
    assert "Lotofácil" in response.get_data(as_text=True)


def test_health_live_returns_ok(client):
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_generate_route_rejects_get_method(client):
    response = client.get("/gerar/megasena")

    assert response.status_code == 405


def test_unknown_lottery_returns_404(client):
    response = client.post(
        "/gerar/quina",
        data={"games": "1", "picks": "6"},
    )

    assert response.status_code == 404
    assert "Modalidade não encontrada." in response.get_data(as_text=True)


@pytest.mark.parametrize(
    ("payload", "expected_message"),
    [
        (
            {"games": "abc", "picks": "6"},
            "Quantidade de jogos deve ser um número inteiro.",
        ),
        (
            {"games": "1", "picks": "abc"},
            "Quantidade de dezenas deve ser um número inteiro.",
        ),
    ],
)
def test_generate_rejects_non_integer_fields(client, payload, expected_message):
    response = client.post("/gerar/megasena", data=payload)

    assert response.status_code == 400
    assert expected_message in response.get_data(as_text=True)


@pytest.mark.parametrize(
    ("payload", "expected_message"),
    [
        (
            {"games": "0", "picks": "6"},
            "Quantidade de jogos deve estar entre 1 e 12.",
        ),
        (
            {"games": "1", "picks": "13"},
            "Quantidade de dezenas deve estar entre 6 e 12.",
        ),
    ],
)
def test_generate_maps_domain_validation_to_400(
    client,
    payload,
    expected_message,
):
    response = client.post("/gerar/megasena", data=payload)

    assert response.status_code == 400
    assert expected_message in response.get_data(as_text=True)


def test_generate_valid_request_returns_result(
    client,
    generation_service_mock,
):
    generation_service_mock.execute.return_value = GenerationResult(
        games=[[1, 2, 3, 4, 5, 6]],
        mode="test",
        source="fake",
        message="Dados de teste.",
    )

    response = client.post(
        "/gerar/megasena",
        data={"games": "1", "picks": "6"},
    )

    assert response.status_code == 200
    assert "Dados de teste." in response.get_data(as_text=True)
    generation_service_mock.execute.assert_called_once_with(
        GenerateGamesRequest(
            lottery=LotteryCode.MEGA_SENA,
            games=1,
            picks=6,
        )
    )


def test_generate_known_service_error_returns_503(
    client,
    generation_service_mock,
):
    generation_service_mock.execute.side_effect = ExternalServiceError(
        "API indisponível."
    )

    response = client.post(
        "/gerar/megasena",
        data={"games": "1", "picks": "6"},
    )

    assert response.status_code == 503
    assert (
        "Não foi possível gerar os jogos agora. Tente novamente."
        in response.get_data(as_text=True)
    )


def test_generate_unexpected_error_returns_500(
    client,
    generation_service_mock,
):
    generation_service_mock.execute.side_effect = RuntimeError(
        "Falha inesperada de teste."
    )

    response = client.post(
        "/gerar/megasena",
        data={"games": "1", "picks": "6"},
    )

    assert response.status_code == 500
    assert (
        "Ocorreu um erro inesperado. Tente novamente."
        in response.get_data(as_text=True)
    )
