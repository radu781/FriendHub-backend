from dataclasses import dataclass, field

import requests

from database.dao.login_location_dao import LoginLocationDAO
from database.objects.login_locations import LoginLocation
from models.user_model import User


@dataclass
class Location:
    country: str
    city: str
    region: str
    isp: str
    ip: str

    def __init__(self, ip: str | None) -> None:
        if ip is None:
            self.country = self.city = self.region = self.isp = self.ip = "???"
            return

        self.ip = ip

        res = requests.get(f"http://ip-api.com/json/{ip}?fields=61439")
        js = res.json()
        if not res.ok or ("status" in js and js["status"] == "fail"):
            self.country = self.city = self.region = self.isp = "???"
            return

        self.country = js["country"]
        self.city = js["city"]
        self.region = js["regionName"]
        self.isp = js["isp"]

    def new(self, user: User) -> None:
        LoginLocationDAO.create(
            LoginLocation(
                user_id=user.id_,
                country=self.country,
                city=self.city,
                region=self.region,
                isp=self.isp,
                ip_address=self.ip,
            )
        )
