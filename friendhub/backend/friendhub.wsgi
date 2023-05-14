#!/usr/bin/python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.append("/var/www/friendhub/")
sys.path.append("/var/www/friendhub/friendhub/")
sys.path.append("/var/www/friendhub/friendhub/backend/")
sys.path.append("/var/www/friendhub/friendhub/backend/src")

from src.main import app as application  # type: ignore
