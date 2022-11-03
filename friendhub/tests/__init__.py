from configparser import ConfigParser
from config_keys import GH_ACTIONS

LOGIN_ENDPOINT = "/api/login"
REGISTER_ENDPOINT = "/api/register"

# github action only
USER_EMAIL = ""
USER_PASSWORD = ""
USER_FIRST_NAME = ""
USER_MIDDLE_NAME = ""
USER_LAST_NAME = ""
USER_COUNTRY = ""
USER_CITY = ""
USER_EDUCATION = ""
USER_EXTRA = ""

if not GH_ACTIONS:
    ini_file = ConfigParser()
    ini_file.read("friendhub/config/testing.ini")

    LOCAL = "http://127.0.0.1"
    HOST = ini_file.get("url", "host") if ini_file.get("deploy", "active") == "1" else LOCAL

    USER_EMAIL = ini_file.get("mock_user", "email")
    USER_PASSWORD = ini_file.get("mock_user", "password")
    USER_FIRST_NAME = ini_file.get("mock_user", "first_name")
    USER_MIDDLE_NAME = ini_file.get("mock_user", "middle_name")
    USER_LAST_NAME = ini_file.get("mock_user", "last_name")
    USER_COUNTRY = ini_file.get("mock_user", "country")
    USER_CITY = ini_file.get("mock_user", "city")
    USER_EDUCATION = ini_file.get("mock_user", "education")
    USER_EXTRA = ini_file.get("mock_user", "extra")
