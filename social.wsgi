#!/usr/bin/python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.append("/var/www/social/")
sys.path.append("/var/www/social/social/")

from social import app as application
