import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable

import logger
from flask.wrappers import Request


class Method(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()


class ArgType(Enum):
    MANDATORY = auto()
    OPTIONAL = auto()
    PREFIX = auto()


@dataclass(frozen=True, eq=True)
class Argument:
    key: str
    type: ArgType
    default_value: Any
    convert_func: Callable[[str], Any] = str


class ArgsNotFoundException(Exception):
    def __init__(self, args: list[str]) -> None:
        super().__init__(args)


@dataclass(frozen=True, eq=True)
class ArgumentParser:
    url: Request
    args: set[Argument]
    method: Method = field(default=Method.GET)

    def parse(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        not_found: list[str] = []

        match self.method:
            case Method.POST | Method.PUT:
                for arg in self.args:
                    if arg.type == ArgType.MANDATORY and not (
                        arg.key in self.url.form or arg.key in self.url.args
                    ):
                        not_found.append(arg.key)
                    elif arg.type == ArgType.PREFIX:
                        for item in self.url.form:
                            if item.find(arg.key) != -1:
                                out[arg.key] = arg.convert_func(item.split(arg.key)[1])
                        for item in self.url.args:
                            if item.find(arg.key) != -1:
                                out[arg.key] = arg.convert_func(self.url.args[item])
                    else:
                        value = self.url.form.get(arg.key, arg.default_value, type=str)
                        if value == arg.default_value:
                            out[arg.key] = arg.convert_func(self.url.args.get(arg.key, arg.default_value, type=str))
                        else:
                            out[arg.key] = arg.convert_func(value)
            case Method.GET:
                for arg in self.args:
                    if arg.type == ArgType.MANDATORY and arg.key not in self.url.args:
                        not_found.append(arg.key)
                    else:
                        logger.debug("argument here: " + str(self.url.args.get(arg.key, arg.default_value, type=str)))
                        logger.debug("type is: " + str(type(self.url.args.get(arg.key, arg.default_value, type=str))))
                        out[arg.key] = arg.convert_func(self.url.args.get(arg.key, arg.default_value, type=str))
                        if out[arg.key] == "":
                            out[arg.key] = arg.convert_func(arg.default_value)
        if not_found != []:
            raise ArgsNotFoundException(not_found)

        out.update(self.__parse_body_as_json())

        return out

    def __parse_body_as_json(self) -> dict[str, Any]:
        if self.url.content_type != "application/json":
            logger.warning(
                f"Parsing request body as json, but content type is {self.url.content_type}"
            )
        return json.loads(self.url.data.decode())
