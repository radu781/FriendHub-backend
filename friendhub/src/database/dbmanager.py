import random
import threading
from configparser import ConfigParser
from dataclasses import dataclass, field
from datetime import datetime
from queue import PriorityQueue

import config_keys
import psycopg2
import psycopg2.extensions


@dataclass
class __DBManager:
    NO_COMMIT_OPERATIONS = ["SELECT", "DESC"]
    NO_FETCH_OPERATIONS = ["INSERT", "DELETE", "UPDATE"]
    cursor: psycopg2.extensions.cursor = field(init=False)

    @dataclass
    class QueueItem:
        statement: str
        values: tuple
        id_: int
        count: int

    DBType = int | float | str | datetime | None

    thread: threading.Thread = field(init=False)
    queue: PriorityQueue[QueueItem] = field(init=False, default=PriorityQueue(-1))
    results: dict[int, list[list[tuple]]] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        ini_file = ConfigParser()
        ini_file.read("config/data.ini")
        self.__restart_connection()
        self.thread = threading.Thread(target=self.__run_forever, name="DBManager")
        self.thread.start()

    def __restart_connection(self) -> None:
        if hasattr(self, "cursor") and not self.cursor:
            self.cursor.close()
        self.connector = psycopg2.connect(
            database=config_keys.DB_SCHEMA,
            user=config_keys.DB_USERNAME,
            password=config_keys.DB_PASSWORD,
            host=config_keys.DB_HOST,
            port=config_keys.DB_PORT,
        )
        self.cursor = self.connector.cursor()

    def __run_forever(self) -> None:
        while True:
            qItem = self.queue.get()
            result = self.__execute(qItem.statement, qItem.values)
            self.queue.task_done()

            if qItem.id_ not in self.results:
                self.results[qItem.id_] = []
            self.results[qItem.id_].append(result)

    def execute(self, statement: str, values: tuple[DBType, ...]) -> list[tuple]:
        id_ = self.__random_id()
        self.queue.put(self.QueueItem(statement, values, id_, 1))
        while id_ not in self.results:
            pass
        while len(self.results[id_]) != 1:
            pass
        ret = self.results[id_][0]
        del self.results[id_]
        return ret

    def execute_multiple(
        self, statement: str, values: list[tuple[DBType, ...]]
    ) -> list[list[tuple[int | str]]]:
        id_ = self.__random_id()
        for value in values:
            self.queue.put(self.QueueItem(statement, value, id_, len(values)))

        while len(self.results[id_]) != len(values):
            pass

        ret = self.results[id_]
        del self.results[id_]
        return ret

    def __execute(
        self, statement: str, values: tuple[int | str | datetime | None, ...]
    ) -> list[tuple]:
        statement = statement.replace("\n", " ").replace("\t", " ").replace("  ", " ")
        try:
            self.cursor.execute(statement, values)
            if statement.split(" ")[0].upper() not in self.NO_COMMIT_OPERATIONS:
                self.connector.commit()
            if statement.split(" ")[0].upper() in self.NO_FETCH_OPERATIONS:
                return []
            return self.cursor.fetchall()
        except psycopg2.Error as ex:
            print(
                f"PostgreSQL error: {ex}, statement: {statement.replace('  ', ' ')}, "
                f"args: {[str(val).strip() for val in values]}"
            )
            if isinstance(ex, psycopg2.OperationalError):
                print("Restarting PostgreSQL connection")
                self.__restart_connection()
                print("Resending values")
                self.execute(statement, values)
            return []

    def __random_id(self) -> int:
        while value := random.randrange(0, 1_000_000):
            if value not in self.results:
                return value
        raise RuntimeError(
            "Unexpected server error: could not generate random id for database operation"
        )


DBManager = __DBManager()
