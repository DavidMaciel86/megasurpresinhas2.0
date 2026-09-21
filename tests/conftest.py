from unittest.mock import Mock

import pytest

from megasurpresinhas2_0.app import create_app
from megasurpresinhas2_0.config import Config


@pytest.fixture()
def app(tmp_path):
    """Cria uma aplicação Flask isolada para cada teste."""
    class TestConfig(Config):
        TESTING = True
        CACHE_DIR = tmp_path

    return create_app(TestConfig)


@pytest.fixture()
def client(app):
    """Disponibiliza o cliente HTTP de testes do Flask."""
    return app.test_client()


@pytest.fixture()
def generation_service_mock(app):
    """Substitui o serviço real para evitar chamadas externas nos testes web."""
    service = Mock(spec_set=["execute"])
    app.extensions["generation_service"] = service
    return service
