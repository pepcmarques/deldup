import json
import os
import sys

from pathlib import Path

from rich.console import Console
from rich.table import Table


console = Console()


cfg_file = "settings.json"

default = {
    "port": 8000,
    "home_dir": f"{Path.home()}",
    "database_url": "sqlite:///./deldup.sqlite3",
    "mode": "none",  # none, db, fs, all
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


if has_settings():
    with open(cfg_file, "r") as cfg:
        settings = json.loads(cfg.read())


def get_categories():
    return settings.get("categories")


def get_database_url():
    return settings.get("database_url")


def get_home_dir():
    return settings.get("home_dir")


def get_category_key_by_code(code):
    for category_key, category_info in settings["categories"].items():
        if category_info["code"] == code:
            return category_key


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


def print_mode_values_table():
    table = Table(title="Possible 'mode' values in settings.json")

    table.add_column("Value", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    
    table.add_row("none", "Remove file visually only")
    table.add_row("db", "Remove file entry from DB.")
    table.add_row("fs", "Remove file from the file system.")
    table.add_row("all", "Remove file entry from DB and remove file from the file system")

    console.print("Mode values documentation")
    console.print(table)


def get_port():
    return settings.get("port", 8000)


if not has_settings():
    console.print("[green]Settings file[/green]", cfg_file, "[green]was[/green] [red bold]not[/][green] found.[/green]")
    console.print("[green]Creating[/green]", cfg_file, "[green]file[/green]")
    with open(cfg_file, "w") as cfg:
        cfg.write(json.dumps(default, indent=4))
    console.print("[green]Please, review the[/green]", cfg_file, "[green]file. Then, run this app again.[/green]")
    print_mode_values_table()
    sys.exit()
