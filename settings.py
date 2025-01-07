import json
import os

from pathlib import Path


cfg_file = "settings.json"

default = {
    "home_dir": f"{Path.home()}",
    "database_url": "sqlite:///./deldup.sqlite3",
    "mode": "none",  # none, db, fs, both
    "categories": {
        "images": {
            "code": "img",
            "ext": [
                "bmp", 
                "gif", 
                "jpg", 
                "jpeg", 
                "png", 
                "tiff"
            ]
        },
        "documents": {
            "code": "doc",
            "ext": [
                "doc",
                "docx", 
                "odt", 
                "ods", 
                "ppt", 
                "pptx", 
                "pdf", 
                "txt",
                "xls", 
                "xlsx"
            ]
        }
    }
}


def has_settings():
    if not os.path.isfile(cfg_file):
        return False
    return True


if not has_settings():
    with open(cfg_file, "w") as cfg:
        cfg.write(json.dumps(default, indent=4))


if has_settings():
    with open(cfg_file, "r") as cfg:
        settings = json.loads(cfg.read())


def get_categories():
    return settings.get("categories")


def get_database_url():
    return settings.get("database_url")


def get_home_dir():
    return settings.get("home_dir")


def get_categories_code():
    return [v["code"] for v in settings["categories"].values()]


def get_extensions(code):
    return [c["ext"] for c in settings["categories"].values() if c["code"] == code][0]


def get_ext_code():
    tmp = {}
    for category in get_categories().values():
        for ext in category["ext"]:
            tmp[ext] = category["code"]
    return tmp


def get_mode():
    return settings.get("mode")
