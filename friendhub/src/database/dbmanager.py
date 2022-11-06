from configparser import ConfigParser
from dataclasses import dataclass, field
from datetime import datetime

import config_keys
import mysql.connector as con
import mysql.connector.connection_cext as connection
from mysql.connector.errors import Error, OperationalError
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
        self.__restart_connection()

    def __restart_connection(self) -> None:
        if hasattr(self, "cursor") and not self.cursor:
            self.cursor.close()
        if hasattr(self, "connector") and not self.connector:
            self.connector.close()
        self.connector: connection.CMySQLConnection = con.connect(  # type: ignore
            database=config_keys.DB_SCHEMA,
            user=config_keys.DB_USERNAME,
            password=config_keys.DB_PASSWORD,
            host=config_keys.DB_HOST,
            port=config_keys.DB_PORT,
        )
        self.cursor = self.connector.cursor()  # type: ignore

    def execute(
        self, statement: str, values: tuple[int | str | datetime | None, ...]
    ) -> list[tuple]:
        statement = statement.replace("\n", " ").replace("  ", " ")
        try:
            self.cursor.execute(statement, values)
            if not statement.split(" ")[0].upper() in ["SELECT", "DESC"]:
                self.connector.commit()
            return self.cursor.fetchall()
        except Error as ex:
            print(
                f"""MySQL error: {ex}, statement: {statement.replace('  ', ' ')},
                args: {[str(val).strip() for val in values]}"""
            )
            if isinstance(ex, OperationalError):
                print("Restarting MySQL connection")
                self.__restart_connection()
            return []

    def execute_multiple(
        self, statement: str, values: list[tuple[int | str | datetime | None, ...]]
    ) -> list[list[tuple[int | str]]]:
        out: list[list[tuple[int | str]]] = []

        for value in values:
            out.append(self.execute(statement, value))

        return out


DBManager = __DBManager()
