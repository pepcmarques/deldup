from sqlmodel import SQLModel

from app import dbengine
from app.models import File

from services import get_codes_in_db, populate_categories
import settings

from rich.console import Console


console = Console()


def init_db():
    console.print("[green]Checking if database exists. If [bold]not[/bold], it will be created[/green]")
    SQLModel.metadata.create_all(dbengine.engine)


def populate_db():
    categories = settings.get_categories()
    categories_txt = ", ".join(categories.keys())
    console.print("[green]Checking if[/green]", categories_txt, "[green]have files. If [bold]not[/bold], it will be created[/green]")
    codes_in_db = get_codes_in_db()
    codes_to_populate = set(settings.get_categories_code()).difference(set(codes_in_db))
    to_populate = []
    for code in codes_to_populate:
        cat_key = settings.get_category_key_by_code(code)
        to_populate.append(categories[cat_key])
    if to_populate:
        populate_categories(to_populate)