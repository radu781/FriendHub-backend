from database.dbmanager import DBManager
from database.objects.login_locations import LoginLocation


class LoginLocationDAO:
    @staticmethod
    def create(location: LoginLocation) -> None:
        DBManager.execute(
            """INSERT INTO login_locations(id, user_id, country, city, region, isp, allowed, timestamp, ip_address)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                str(location.id_),
                str(location.user_id),
                location.country,
                location.city,
                location.region,
                location.isp,
                location.allowed,
                location.timestamp,
                location.ip_address,
            ),
        )

    @staticmethod
    def known_ip(ip: str | None) -> bool:
        if ip is None:
            return False
        result = DBManager.execute("""SELECT * FROM login_locations WHERE ip_address = %s""", (ip,))
        return len(result) > 0
