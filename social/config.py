from configparser import ConfigParser
import os

pwd = os.getcwd()
print(pwd)
ini_file = ConfigParser()
ini_file.read("social/config/data.ini")

SESSION_KEY = ini_file.get("pages", "key")
DEPLOY_KEY = ini_file.get("deploy", "key")
DEBUG_ON = True if ini_file.get("pages", "debug") == 1 else False
