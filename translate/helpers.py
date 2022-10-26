from datetime import datetime
import os
import threading

import multiprocessing
import translators as ts

from config import *

failed_translations: set[tuple[str, Exception]] = set()
WAIT_TIME_SEC = 10


def setup() -> None:
    try:
        os.mkdir("friendhub/translations")
    except FileExistsError:
        pass
    os.system("pybabel extract -F friendhub/babel.cfg -o friendhub/translations/messages.pot .")
    file_lines: list[str] = []
    with open("friendhub/translations/messages.pot") as messages:
        file_lines = messages.readlines()

    new_file_lines: list[str] = []
    for index, line in enumerate(file_lines):
        if index < 20:
            new_file_lines.append(
                line.replace("PROJECT", PROJECT)
                .replace("ORGANIZATION", ORGANIZATION)
                .replace("FIRST AUTHOR", AUTHOR)
                .replace("EMAIL@ADDRESS", EMAIL)
                .replace("VERSION", VERSION)
                .replace("FULL NAME", AUTHOR)
                .replace("YEAR-MO-DA HO:MI+ZONE", str(datetime.now())[:-10] + "+0300")
            )
        else:
            new_file_lines.append(line)

    new_file_content = "".join(new_file_lines)
    try:
        with open("friendhub/translations/messages.pot", "wb") as file:
            file.write(new_file_content.encode("utf-8"))
    except Exception:
        pass


def translate_and_replace(language: str, file_path: str) -> None:
    file_lines: list[str] = []
    with open(file_path) as file:
        file_lines = file.readlines()

    return_file: list[str] = []
    for index, line in enumerate(file_lines):
        if line.find("msgstr") == -1:
            return_file.append(line)
        if line.find("msgstr") == 0 and len(line) == 10 and index < 10:
            return_file.append(line)
        if line.find("msgid") != -1 and len(line) > 9:
            msgid = line[len("msgid") + 2 : -2]
            try:
                return_file.append(f'msgstr "{str(ts.google(msgid, to_language=language))}"\n')
            except Exception as ex:
                with threading.Lock():
                    failed_translations.add((language, ex))
                return
    new_file_content = "".join(return_file)
    try:
        with open(file_path, "wb") as file:
            file.write(new_file_content.encode("utf-8"))
    except Exception:
        pass


def treat_language(language: str) -> None:
    os.system(
        f"pybabel init -i friendhub/translations/messages.pot -d friendhub/translations/ -l {language}"
    )
    file_path = f"friendhub/translations/{language}/LC_MESSAGES/messages.po"

    try:
        os.mkdir(f"friendhub/translations/{language}")
        os.mkdir(f"friendhub/translations/{language}/LC_MESSAGES")
    except FileExistsError:
        pass
    translate_and_replace(language, file_path)


def spawn_threads_and_work(languages: set[str]) -> None:
    processes: list[multiprocessing.Process] = []
    for language in languages:
        processes.append(multiprocessing.Process(target=treat_language, args=(language,)))
    for process in processes:
        process.start()
    for process in processes:
        process.join()
