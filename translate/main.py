import os
from time import sleep

from helpers import *


def main() -> None:
    languages: set[str] = {
        "ru",
        "es",
        "de",
        "tr",
        "fr",
        "ja",
        "ko",
        "ro",
        "az",
        "zh",
        "hi",
        "ar",
        "bn",
        "pt",
        "id"
    }
    setup()
    spawn_threads_and_work(languages)

    while failed_translations != set():
        print(f"{failed_translations=}, retrying in {WAIT_TIME_SEC} sec")
        sleep(WAIT_TIME_SEC)
        spawn_threads_and_work(set(tr[0] for tr in failed_translations))
    os.system("pybabel compile -d friendhub/translations/")


if __name__ == "__main__":
    main()
