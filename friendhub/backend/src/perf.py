import os
import re
import shutil
import time
from typing import Never

from flask import Flask
from werkzeug.middleware.profiler import ProfilerMiddleware


def profile(app: Flask) -> None:
    try:
        shutil.rmtree("friendhub/backend/performance/", ignore_errors=True)
        os.mkdir("friendhub/backend/performance/")
    except (FileNotFoundError, FileExistsError):
        pass

    app.config["PROFILE"] = True
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app,
        restrictions=[10],
        profile_dir="friendhub/backend/performance/",
        stream=None,  # type:ignore
    )


def move_files() -> Never:
    api_endpoints = ["root", "api", "profile", "post", "docs"]
    while True:
        for file in os.listdir("friendhub/backend/performance/"):
            file_path = f"friendhub/backend/performance/{file}"
            for endpoint in api_endpoints:
                if re.match(rf"^(GET|POST|PUT|DELETE).{endpoint}", file):
                    try:
                        os.renames(file_path, f"friendhub/backend/performance/api/{file}")
                    except PermissionError:
                        continue
            if "static" in file.lower() or "_jstrans" in file.lower():
                try:
                    os.renames(file_path, f"friendhub/backend/performance/static/{file}")
                except PermissionError:
                    continue
        time.sleep(3)
