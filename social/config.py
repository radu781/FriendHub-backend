from configparser import ConfigParser

ini_file = ConfigParser()
ini_file.read("social/config/data.ini")

SESSION_KEY = ini_file.get("pages", "key")
DEBUG_ON = True if ini_file.get("pages", "debug") == "1" else False

DEPLOY_KEY = ini_file.get("deploy", "key")
DEPLOYING = True if ini_file.get("deploy", "active") == "1" else False
