from configparser import ConfigParser
from dataclasses import dataclass, field

import config
import mysql.connector as con
import mysql.connector.connection_cext as connection
import mysql.connector.cursor_cext as _cursor


@dataclass
class __DBManager:
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
        self, statement: str, values: tuple[int | str | None, ...]
    ) -> list[tuple]:
        try:
            self.cursor.execute(statement, values)
            if not statement.split(" ")[0].upper() == "SELECT":
                self.connector.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print(e, "statement:", statement, sep="\n")
            return []

    def execute_multiple(
        self, statement: str, values: list[tuple[int | str | None, ...]]
    ) -> list[list[tuple[int | str]]]:
        out: list[list[tuple[int | str]]] = []

        for value in values:
            out.append(self.execute(statement, value))

        return out


DBManager = __DBManager()
