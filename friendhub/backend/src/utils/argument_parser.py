import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any

import logger
from flask.wrappers import Request


class Method(Enum):
    GET = auto()
    POST = auto()


class ArgType(Enum):
    MANDATORY = auto()
    OPTIONAL = auto()
    PREFIX = auto()


@dataclass(frozen=True, eq=True)
class Argument:
    key: str
    type: ArgType
    default_value: Any


class ArgsNotFoundException(Exception):
    def __init__(self, args: list[str]) -> None:
        super().__init__(args)


@dataclass(frozen=True, eq=True)
class ArgumentParser:
    url: Request
    args: set[Argument]
    method: Method = field(default=Method.GET)

    def parse(self) -> dict[str, str]:
        out: dict[str, str] = {}
        not_found: list[str] = []

        match self.method:
            case Method.POST:
                for arg in self.args:
                    if arg.type == ArgType.MANDATORY and not (
                        arg.key in self.url.form or arg.key in self.url.args
                    ):
                        not_found.append(arg.key)
                    elif arg.type == ArgType.PREFIX:
                        for item in self.url.form:
                            if item.find(arg.key) != -1:
                                out[arg.key] = item.split(arg.key)[1]
                        for item in self.url.args:
                            if item.find(arg.key) != -1:
                                out[arg.key] = self.url.args[item]
                    else:
                        value = self.url.form.get(arg.key, arg.default_value, type=str)
                        if value == arg.default_value:
                            out[arg.key] = self.url.args.get(arg.key, arg.default_value, type=str)
                        else:
                            out[arg.key] = value
            case Method.GET:
                for arg in self.args:
                    if arg.type == ArgType.MANDATORY and arg.key not in self.url.args:
                        not_found.append(arg.key)
                    else:
                        out[arg.key] = self.url.args.get(arg.key, arg.default_value, type=str)
                        if out[arg.key] == "":
                            out[arg.key] = arg.default_value
        if not_found != []:
            raise ArgsNotFoundException(not_found)

        return out

    def parse_body_as_text(self) -> str:
        return self.url.data.decode()

    def parse_body_as_json(self) -> dict[str, Any]:
        if self.url.content_type != "application/json":
            logger.warning(
                f"Parsing request body as json, but content type is {self.url.content_type}"
            )
        return json.loads(self.url.data.decode())
