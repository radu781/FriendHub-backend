import subprocess
from dataclasses import dataclass
from uuid import UUID
import logger


@dataclass
class Location:
    country: str
    city: str
    region: str
    isp: str


@dataclass
class Email:
    @staticmethod
    def __handle_output(output: subprocess.CompletedProcess[bytes], to: str) -> None:
        if output.returncode != 0:
            logger.warning("Send error: " + str(output.stderr, encoding="utf-8"), logger.LogCategory.EMAIL)
        else:
            logger.debug(f"Sent successfully for {to}", logger.LogCategory.EMAIL)

    @staticmethod
    def welcome(to: str, id_: UUID, name: str):
        output = subprocess.run(
            f"./bin/email/email welcome --to {to} --full-name {name} --id {id_}"
        )
        Email.__handle_output(output, to) 

    @staticmethod
    def password_reset(to: str, id_: UUID, name: str, token: str):
        exit_code, output = subprocess.getstatusoutput(
            [
                "./bin/email",
                "password-reset",
                "--to",
                to,
                "--full-name",
                name,
                "--id",
                str(id_),
                "--token",
                token,
            ]
        )
        if exit_code != 0:
            logger.warning(output, logger.LogCategory.EMAIL)

    @staticmethod
    def new_login(to: str, name: str, location: Location):
        command = f"./bin/email/email new-login --to {to} --full-name {name} --country {location.country} --city {location.city} --region {location.region} --isp {location.isp}"
        output = subprocess.run(command)
        Email.__handle_output(output, to)

    @staticmethod
    def birthday(to: str, id_: UUID, name: str):
        exit_code, output = subprocess.getstatusoutput(
            [
                "./bin/email",
                "birthday",
                "--to",
                to,
                "--full-name",
                name,
                "--id",
                str(id_),
            ]
        )
        if exit_code != 0:
            logger.warning(output, logger.LogCategory.EMAIL)
