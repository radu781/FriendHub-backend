import base64
import os

GH_ACTIONS = "GH_ACTIONS_ENV" in os.environ

if GH_ACTIONS:
    DB_HOST = os.environ["DB_HOST"]
    DB_SCHEMA = os.environ["DB_SCHEMA"]
    DB_USERNAME = os.environ["DB_USERNAME"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]
    DB_PORT = os.environ["DB_PORT"]
else:
    import sys
    from configparser import ConfigParser

    if sys.platform in ("linux", "linux2"):
        os.chdir("/var/www/friendhub")
    ini_file = ConfigParser()
    ini_file.read("friendhub/config/data.ini")

    SESSION_KEY = ini_file.get("pages", "key")

    DEBUG_ON = ini_file.get("pages", "debug") == "1"

    DEPLOY_KEY = ini_file.get("deploy", "key")
    DEPLOYING = ini_file.get("deploy", "active") == "1"

    DB_HOST = ini_file.get("database", "host")
    DB_SCHEMA = ini_file.get("database", "schema")
    DB_USERNAME = ini_file.get("database", "username")
    DB_PASSWORD = ini_file.get("database", "password")
    DB_PORT = ini_file.get("database", "port")

    DELETE_PROFILE_KEY = ini_file.get("admin", "delete_profile")
    SAFE_IPS = ini_file.get("admin", "safe_ips").split(",")

    FERNET_KEY = base64.b64encode(ini_file.get("fernet", "key_hex").encode("utf-8"))
