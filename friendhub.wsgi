#!/usr/bin/python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.append("/var/www/friendhub/")
sys.path.append("/var/www/friendhub/friendhub/")

from friendhub import app as application
