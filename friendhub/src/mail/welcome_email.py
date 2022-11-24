from dataclasses import dataclass

from flask import render_template
from mail.email import Email
from models.user_model import User


@dataclass
class WelcomeEmail(Email):
    user: User

    def __post_init__(self) -> None:
        self.html = render_template("email/welcome.html", user=self.user)
        super().__post_init__()

    def format(self) -> Email:
        return self
