import json


def write_json(info: dict, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(info, file, indent=4, ensure_ascii=False)


def read_json(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)
