#!/usr/bin/python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.append("/var/www/friendhub/")
sys.path.append("/var/www/friendhub/friendhub/")
sys.path.append("/var/www/friendhub/friendhub/src")

from src import app as application  # type: ignore
