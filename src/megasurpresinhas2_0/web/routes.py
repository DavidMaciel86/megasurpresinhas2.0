import logging
from flask import Blueprint, current_app, jsonify, render_template, request, send_from_directory
from megasurpresinhas2_0.application.dto import GenerateGamesRequest
from megasurpresinhas2_0.domain.exceptions import MegaSurpresinhasError, ValidationError
from megasurpresinhas2_0.domain.models import LOTTERIES, LotteryCode

web = Blueprint("web", __name__)
logger = logging.getLogger(__name__)


def _parse_integer(field: str, label: str) -> int:
    value = request.form.get(field, "").strip()
    try:
        return int(value)
    except ValueError as exc:
        raise ValidationError(f"{label} deve ser um número inteiro.") from exc


def _page(code: LotteryCode, **context):
    rules = LOTTERIES[code]
    defaults = {"rules": rules, "result": None, "error": None}
    defaults.update(context)
    return render_template("index.html", **defaults)


@web.get("/")
def mega_sena():
    return _page(LotteryCode.MEGA_SENA)


@web.get("/lotofacil")
def lotofacil():
    return _page(LotteryCode.LOTOFACIL)


@web.post("/gerar/<lottery_code>")
def generate(lottery_code: str):
    try:
        code = LotteryCode(lottery_code)
    except ValueError:
        return render_template("error.html", message="Modalidade não encontrada."), 404
    try:
        games = _parse_integer("games", "Quantidade de jogos")
        picks = _parse_integer("picks", "Quantidade de dezenas")
        result = current_app.extensions["generation_service"].execute(GenerateGamesRequest(code, games, picks))
        return _page(code, result=result, submitted_games=games, submitted_picks=picks)
    except ValidationError as exc:
        return _page(code, error=str(exc)), 400
    except MegaSurpresinhasError:
        logger.exception("Falha conhecida ao gerar jogos de %s.", code)
        return _page(code, error="Não foi possível gerar os jogos agora. Tente novamente."), 503
    except Exception:
        logger.exception("Falha inesperada ao gerar jogos de %s.", code)
        return _page(code, error="Ocorreu um erro inesperado. Tente novamente."), 500


@web.get("/health/live")
def health_live():
    return jsonify(status="ok")


@web.get("/offline")
def offline():
    return render_template("offline.html")


@web.get("/sw.js")
def service_worker():
    response = send_from_directory(current_app.static_folder, "js/sw.js")
    response.headers["Cache-Control"] = "no-cache"
    return response
