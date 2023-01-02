import os
import re
import shutil
import time

from flask import Flask
from werkzeug.middleware.profiler import ProfilerMiddleware


def profile(app: Flask) -> None:
    try:
        shutil.rmtree("friendhub/performance/", ignore_errors=True)
        os.mkdir("friendhub/performance/")
    except (FileNotFoundError, FileExistsError):
        pass

    app.config["PROFILE"] = True
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app,
        restrictions=[10],
        profile_dir="friendhub/performance/",
        stream=None,  # type:ignore
    )


def move_files() -> None:
    api_endpoints = ["root", "api", "profile", "post", "docs"]
    while True:
        for file in os.listdir("friendhub/performance/"):
            file_path = f"friendhub/performance/{file}"
            for endpoint in api_endpoints:
                if re.match(rf"^(GET|POST|PUT|DELETE).{endpoint}", file):
                    try:
                        os.renames(file_path, f"friendhub/performance/api/{file}")
                    except PermissionError:
                        continue
            if "static" in file.lower() or "_jstrans" in file.lower():
                try:
                    os.renames(file_path, f"friendhub/performance/static/{file}")
                except PermissionError:
                    continue
        time.sleep(3)
