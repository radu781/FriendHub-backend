from configparser import ConfigParser
from dataclasses import dataclass, field

import config
import mysql.connector as con
import mysql.connector.connection_cext as connection
import mysql.connector.cursor_cext as _cursor


@dataclass
class DBManager:
    connector: connection.CMySQLConnection = field(
        init=False, default=connection.CMySQLConnection()
    )
    cursor: _cursor.CMySQLCursor = field(init=False)

    def __post_init__(self) -> None:
        ini_file = ConfigParser()
        ini_file.read("config/data.ini")
        self.connector: connection.CMySQLConnection = con.connect(  # type: ignore
            database=config.DB_SCHEMA,
            user=config.DB_USERNAME,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
        )
        self.cursor = self.connector.cursor()  # type: ignore

    def execute(
        self, statement: str, values: dict[str, int | str | None]
    ) -> list[tuple]:
        pretty_statement = self.__assign(statement, values)
        try:
            self.cursor.execute(pretty_statement)
            if not pretty_statement.split(" ")[0].upper() == "SELECT":
                self.connector.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print(e, "statement:", pretty_statement, sep="\n")
            return []

    def execute_multiple(
        self, statement: str, values: list[dict[str, int | str | None]]
    ) -> list[list[tuple[int | str]]]:
        out: list[list[tuple[int | str]]] = []

        pretty_statements = self.__assign_multiple(statement, values)
        for item in pretty_statements:
            out.append(self.execute(item, {}))

        return out

    def __assign(
        self,
        statement: str,
        values: dict[str, int | str | None],
    ) -> str:
        out = statement.replace("\n", " ").replace("\t", " ").replace("  ", " ")

        for value in values.keys():
            if isinstance(values[value], int):
                prepared_value = str(values[value])
            elif isinstance(values[value], str):
                percentage = out.index(f":{value}") - 1
                if percentage >= 0 and out[percentage] == "%":
                    prepared_value = f"'%{values[value]}%'"
                    out = out.replace(f"%:{value}%", f":{value}")
                else:
                    prepared_value = f"'{values[value]}'"
            else:
                prepared_value = "NULL"
            out = out.replace(f":{value}", prepared_value)

        return out

    def __assign_multiple(
        self,
        statement: str,
        values: list[dict[str, int | str | None]],
    ) -> list[str]:
        out: list[str] = []

        for line in values:
            out.append(self.__assign(statement, line))

        return out
