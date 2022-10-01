from configparser import ConfigParser

ini_file = ConfigParser()
ini_file.read("friendhub/config/translations.ini")

PROJECT = ini_file.get("pot", "project")
ORGANIZATION = ini_file.get("pot", "organization")
AUTHOR = ini_file.get("pot", "first_author")
EMAIL = ini_file.get("pot", "email")
VERSION = ini_file.get("pot", "version")
