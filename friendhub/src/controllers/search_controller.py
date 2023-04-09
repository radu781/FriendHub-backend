from json.decoder import JSONDecodeError
from typing import Any

from database.search_dao import SearchDAO
from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status
from utils.argument_parser import ArgsNotFoundException, ArgType, Argument, ArgumentParser, Method

search_blueprint = Blueprint("search_blueprint", __name__)

__allowed_filters: list[str] = ["user", "page"]


@search_blueprint.route("/api/search", methods=["GET"])
def search() -> Response:
    parser = ArgumentParser(
        request,
        {Argument("query", ArgType.MANDATORY, ""), Argument("max", ArgType.OPTIONAL, 10)},
        Method.GET,
    )
    try:
        values = parser.parse()
    except ArgsNotFoundException as ex:
        return make_response(
            jsonify({"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}),
            status.HTTP_400_BAD_REQUEST,
        )
    try:
        body = parser.parse_body_as_json()
    except JSONDecodeError as ex:
        return make_response(
            jsonify({"error": "json body decode error", "reason": str(ex)}),
            status.HTTP_400_BAD_REQUEST,
        )
    if "type" not in body:
        return make_response(
            jsonify({"reason": "expected 'type' in request body"}),
            status.HTTP_400_BAD_REQUEST,
        )
    if not isinstance(body["type"], list) or len(body["type"]) == 0:
        return make_response(
            jsonify({"reason": "'type' is either not an array or has length 0"}),
            status.HTTP_400_BAD_REQUEST,
        )

    unknown_types: list[str] = []
    for type_ in body["type"]:
        if type_ not in __allowed_filters:
            unknown_types.append(type_)
    if unknown_types != []:
        return make_response(
            jsonify(
                {
                    "allowedTypes": __allowed_filters,
                    "reason": "found unknown filter types",
                    "unknown": unknown_types,
                }
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    result = __build_response(body["type"], values)
    return make_response(jsonify(result), status.HTTP_200_OK)


def __build_response(types: list[str], query_values: dict[str, str]) -> dict[str, Any]:
    result: dict[str, Any] = {}

    if "user" in types:
        users_found = SearchDAO.search_name(query_values["query"], int(query_values["max"]))
        result["users"] = {}
        result["users"]["count"] = len(users_found)
        result["users"]["data"] = (
            list(vars(user.sanitize()) for user in users_found) if len(users_found) > 0 else []
        )
    if "page" in types:
        pages_found = SearchDAO.search_page(query_values["query"], int(query_values["max"]))
        result["pages"] = {}
        result["pages"]["count"] = len(pages_found)
        result["pages"]["data"] = (
            list(vars(page for page in pages_found)) if len(pages_found) > 0 else []
        )

    return result
