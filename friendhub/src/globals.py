import sys
from configparser import ConfigParser

if sys.platform == "linux" or sys.platform == "linux2":
    import os

    os.chdir("/var/www/friendhub")

ini_file = ConfigParser()
ini_file.read("friendhub/config/data.ini")

SESSION_KEY = ini_file.get("pages", "key")
DEBUG_ON = True if ini_file.get("pages", "debug") == "1" else False

DEPLOY_KEY = ini_file.get("deploy", "key")
DEPLOYING = True if ini_file.get("deploy", "active") == "1" else False

DB_HOST = ini_file.get("database", "host")
DB_SCHEMA = ini_file.get("database", "schema")
DB_USERNAME = ini_file.get("database", "username")
DB_PASSWORD = ini_file.get("database", "password")
DB_PORT = ini_file.get("database", "port")
