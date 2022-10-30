import os
from configparser import ConfigParser

if os.path.exists("friendhub/config/testing.ini"):
    ini_file = ConfigParser()
    ini_file.read("friendhub/config/testing.ini")

    LOCAL = "http://127.0.0.1"
    HOST = ini_file.get("url", "host") if ini_file.get("deploy", "active") == "1" else LOCAL
    LOGIN_ENDPOINT = HOST + ini_file.get("url", "login")
    REGISTER_ENDPOINT = HOST + ini_file.get("url", "register")

    USER_EMAIL = ini_file.get("mock_user", "email")
    USER_PASSWORD = ini_file.get("mock_user", "password")
    USER_FIRST_NAME = ini_file.get("mock_user", "first_name")
    USER_MIDDLE_NAME = ini_file.get("mock_user", "middle_name")
    USER_LAST_NAME = ini_file.get("mock_user", "last_name")
    USER_COUNTRY = ini_file.get("mock_user", "country")
    USER_CITY = ini_file.get("mock_user", "city")
    USER_EDUCATION = ini_file.get("mock_user", "education")
    USER_EXTRA = ini_file.get("mock_user", "extra")
