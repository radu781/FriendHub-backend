import datetime
from typing import Any

from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from flask_api import status

import logger
from database.search_dao import SearchDAO
from utils.argument_parser import (ArgsNotFoundException, ArgType, Argument,
                                   ArgumentParser, Method)

search_blueprint = Blueprint("search_blueprint", __name__)

__allowed_filters: list[str] = ["user", "page", "groups", "posts"]


@search_blueprint.route("/api/search", methods=["GET"])
def search() -> Response:
    parser = ArgumentParser(
        request,
        {
            Argument("query", ArgType.MANDATORY, ""),
            Argument("max", ArgType.OPTIONAL, 10),
            Argument("contains", ArgType.OPTIONAL, ""),
            Argument(
                "created-after",
                ArgType.OPTIONAL,
                "1970-01-01T00:00:00Z",
                datetime.datetime.fromisoformat,
            ),
            Argument(
                "created-before",
                ArgType.OPTIONAL,
                datetime.datetime.isoformat(datetime.datetime.today() + datetime.timedelta(days=1)),
                datetime.datetime.fromisoformat,
            ),
        },
        Method.GET,
    )
    try:
        values = parser.parse()
    except ArgsNotFoundException as ex:
        return make_response(
            jsonify({"reason": "missing parameters", "parameters": ", ".join(ex.args[0])}),
            status.HTTP_400_BAD_REQUEST,
        )
    if "type" not in values:
        return make_response(
            jsonify({"reason": "expected 'type' in request body"}),
            status.HTTP_400_BAD_REQUEST,
        )
    if not isinstance(values["type"], list) and len(values["type"]) == 0:
        return make_response(
            jsonify({"reason": "'type' is either not an array or has length 0"}),
            status.HTTP_400_BAD_REQUEST,
        )

    unknown_types: list[str] = []
    if isinstance(values["type"], str):
        values["type"] = [values["type"]]
    for type_ in values["type"]:
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

    result = __build_response(values)
    return make_response(jsonify(result), status.HTTP_200_OK)


def __build_response(
    query_values: dict[str, str],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    item_types = query_values["type"]
    query = query_values["query"]
    max_search_value = int(query_values["max"])
    AFTER: datetime.datetime = query_values["created-after"]  # type: ignore
    BEFORE: datetime.datetime = query_values["created-before"]  # type: ignore

    if "user" in item_types:
        __handle_user_find(result, query_values, max_search_value)

    if "page" in item_types:
        __handle_page_find(result, query_values, max_search_value)

    if "groups" in item_types:
        __handle_groups_find(result, query_values, max_search_value)

    if "posts" in item_types:
        __handle_post_find(result, query_values, max_search_value)

    return result


def __handle_user_find(
    result_in_out: dict[str, Any], query_values: dict[str, str], limit: int
) -> None:
    users_found = SearchDAO.search_name(query_values["query"], limit)
    result_in_out["users"] = {}
    result_in_out["users"]["count"] = len(users_found)
    found_users = (
        list(vars(user.sanitize()) for user in users_found) if len(users_found) > 0 else []
    )

    if "contains" in query_values and query_values["contains"] != "":
        sub_profile_matches = SearchDAO.search_profile_description(query_values["query"], limit)
        matches = (
            list(vars(user.sanitize()) for user in sub_profile_matches)
            if len(sub_profile_matches) > 0
            else []
        )
        found_users = list(set(result_in_out["users"]["data"]) | set(matches))

    result_in_out["users"]["data"] = found_users


def __handle_page_find(
    result_in_out: dict[str, Any], query_values: dict[str, str], limit: int
) -> None:
    pages_found = SearchDAO.search_page(query_values["query"], limit)
    result_in_out["pages"] = {}
    result_in_out["pages"]["count"] = len(pages_found)
    result_in_out["pages"]["data"] = (
        list(vars(page) for page in pages_found) if len(pages_found) > 0 else []
    )
    # TODO: add logic for page description


def __handle_groups_find(
    result_in_out: dict[str, Any], query_values: dict[str, str], limit: int
) -> None:
    pages_found = SearchDAO.search_groups(query_values["query"], limit)
    result_in_out["groups"] = {}
    result_in_out["groups"]["count"] = len(pages_found)
    result_in_out["groups"]["data"] = (
        list(vars(page) for page in pages_found) if len(pages_found) > 0 else []
    )
    # TODO: add logic for group description


def __handle_post_find(
    result_in_out: dict[str, Any], query_values: dict[str, str], limit: int
) -> None:
    posts_found = SearchDAO.search_posts(
        query_values["query"],
        limit,
        query_values["created-after"], # type: ignore
        query_values["created-before"], # type: ignore
        False,
        False,
        False,
    )
    result_in_out["posts"] = {}
    result_in_out["posts"]["count"] = len(posts_found)
    result_in_out["posts"]["data"] = (
        list(vars(post) for post in posts_found) if len(posts_found) > 0 else []
    )
    logger.debug("posts are: " + str(posts_found))
