from sqlmodel import SQLModel

from app import dbengine
from app.models import File

from services import get_categories_in_db, populate_categories
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
    categories_in_db = get_categories_in_db()
    categories_to_populate = set(settings.get_categories_code()).difference(set(categories_in_db))
    to_populate = []
    for category in categories_to_populate:
        to_populate.append(categories[category])
    if to_populate:
        print(to_populate)
        populate_categories(to_populate)