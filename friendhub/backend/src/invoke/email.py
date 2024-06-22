import os
import subprocess
import threading
from dataclasses import dataclass, field
from queue import Empty, PriorityQueue
from typing import Never
from uuid import UUID

import logger
from models.location import Location


@dataclass
class Email:
    @staticmethod
    def welcome(to: str, id_: UUID, name: str):
        cmd = f"./bin/email/email welcome --to {to} --full-name {name} --id {id_}"
        EmailScheduler.enqueue(cmd)

    @staticmethod
    def password_reset(to: str, id_: UUID, name: str, token: str):
        cmd = f"./bin/email/email password-reset --to {to} --full-name {name} --id {id_} --token {token}"
        EmailScheduler.enqueue(cmd)

    @staticmethod
    def new_login(to: str, name: str, location: Location):
        cmd = f"./bin/email/email new-login --to {to} --full-name {name} --country {location.country} --city {location.city} --region {location.region} --isp {location.isp}"
        EmailScheduler.enqueue(cmd)

    @staticmethod
    def birthday(to: str, id_: UUID, name: str):
        cmd = f"./bin/email/email birthday --to {to} --full-name {name} --id {id_}"
        EmailScheduler.enqueue(cmd)


@dataclass
class __EmailScheduler:
    @dataclass
    class QueueItem:
        command: str
        retry_count: int
        MAX_RETRIES: int = 5

    thread: threading.Thread = field(init=False)
    queue: PriorityQueue[QueueItem] = field(init=False, default=PriorityQueue(-1))

    def __post_init__(self) -> None:
        logger.debug(str(threading.get_ident()))
        self.thread = threading.Thread(target=self.__run_forever, name="EmailScheduler")
        self.thread.start()

    def enqueue(self, cmd: str) -> None:
        self.queue.put(self.QueueItem(cmd, 0))

    def __run_forever(self) -> Never:
        while True:
            try:
                qItem = self.queue.get(timeout=3)
                result = self.__execute(qItem.command)

                if result.returncode in (3, 5, 6):
                    email_type = qItem.command.split(" ")[1]
                    if qItem.retry_count >= self.QueueItem.MAX_RETRIES:
                        logger.error(
                            f"Failed to send email of {email_type=} after {qItem.retry_count} retries",
                            logger.LogCategory.EMAIL,
                        )
                    else:
                        logger.warning(
                            f"Failed to send email of {email_type=}, {qItem.retry_count=}: {result.stderr}",
                            logger.LogCategory.EMAIL,
                        )
                        qItem.retry_count += 1
                        self.queue.put(qItem)
                elif result.returncode == 0 or result.returncode is None:
                    logger.debug("Email sent successfully", logger.LogCategory.EMAIL)
            except Empty:
                pass

    def __execute(self, cmd: str) -> subprocess.Popen[bytes]:
        cmd = os.getcwd() + cmd
        cwd = os.getcwd() + "./bin/email"
        return subprocess.Popen(cmd.split(" "), shell=True, cwd=cwd)


EmailScheduler = __EmailScheduler()
logger.debug("EmailScheduler instance created", logger.LogCategory.EMAIL)
