import logging

from flask import Flask

from .application.generation_service import GenerationService
from .config import Config
from .domain.generator import WeightedGameGenerator
from .infrastructure.api_client import GuidiLotteryApiClient
from .infrastructure.cache_repository import JsonCacheRepository
from .web.routes import web


def create_app(config_object=Config) -> Flask:
    app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
    app.config.from_object(config_object)
    logging.basicConfig(level=app.config["LOG_LEVEL"], format="%(asctime)s %(levelname)s %(name)s %(message)s")

    provider = GuidiLotteryApiClient(app.config["API_BASE_URL"], app.config["API_TIMEOUT"])
    cache = JsonCacheRepository(app.config["CACHE_DIR"])
    app.extensions["generation_service"] = GenerationService(provider, cache, WeightedGameGenerator(), app.logger)
    app.register_blueprint(web)

    @app.after_request
    def security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        response.headers.setdefault("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self'; manifest-src 'self'; connect-src 'self'")
        return response

    return app
