import os
import translators as ts


def setup() -> None:
    try:
        os.mkdir("friendhub/translations")
    except FileExistsError:
        pass
    os.system(
        "pybabel extract -F friendhub/babel.cfg -o friendhub/translations/messages.pot ."
    )


def translate_and_replace(language: str, file_path: str):
    file_lines: list[str] = []
    with open(file_path) as file:
        file_lines = file.readlines()

    return_file: list[str] = []
    for line in file_lines:
        if line.find("msgstr") == -1:
            return_file.append(line)
        if line.find("msgid") != -1 and len(line) > 9:
            msgid = line[len("msgid") + 2 : -2]
            return_file.append(
                f'msgstr "{str(ts.google(msgid, to_language=language))}"\n'
            )
    new_file_content = "".join(return_file)
    try:
        with open(file_path, "wb") as file:
            file.write(new_file_content.encode("utf-8"))
    except Exception:
        pass


def main() -> None:
    languages: list[str] = [
        "ru",
        "es",
        "de",
        "tr",
        "fr",
        "ja",
        "ko",
        "ro",
    ]
    setup()
    for language in languages:
        os.system(
            f"pybabel init -i friendhub/translations/messages.pot -d friendhub/translations/ -l {language}"
        )
        file_path = f"friendhub/translations/{language}/LC_MESSAGES/messages.po"

        translate_and_replace(language, file_path)

    os.system("pybabel compile -d friendhub/translations/")


if __name__ == "__main__":
    main()
