import os
from pathlib import Path
import sys
import hashlib
import time

from fastapi import HTTPException
from sqlmodel import select

from app.dbengine import get_session
from app.models import File

from rich.console import Console
from rich.progress import track

import settings


# TODO: Work with threads...
# TODO: To have a type of gitignore file

console = Console()
BUF_SIZE = 65536


def has_files_in_db(code):
    session = get_session()
    result = session.exec(select(File).where(File.filetype == code).limit(1)).all()
    return len(result) > 0


def is_to_ignore(path):
    path_pieces = path.path.split(os.sep)
    for path_piece in path_pieces:
        if path_piece.startswith("."):
            return True
    return False


def is_valid_file(entry, extensions):
    if not entry:
        return False
    if is_to_ignore(entry):
        return False
    ext = entry.name.split(".")[-1]
    if not ext in extensions:
        return False
    return True


def scantree(path):
    try:
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from scantree(entry.path)
            else:
                yield entry
    except PermissionError:
        yield None


def populate_files(extensions_dict):
    extensions = extensions_dict.keys()

    n = 0
    #for dirpath, dirnames, filenames in os.walk(settings.get_home_dir()):
    for entry in track(scantree(settings.get_home_dir())):
        if not is_valid_file(entry, extensions):
            continue
        if not entry.is_file():
            continue
        md5 = hashlib.md5()
        #sha1 = hashlib.sha1()
        try:
            with open(entry, "rb") as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    md5.update(data)
                    #sha1.update(data)
        except PermissionError:
            console.print("")
            console.print("[red]Unable to open:[/red]")
            console.print("  -", entry.path)
            continue
        
        ext = entry.name.split(".")[-1]
        code = extensions_dict[ext]
        file = File(name=entry.name, path=entry.path, filetype=code, fileext=ext, filehash=md5.hexdigest())

        session = get_session()
        session.add(file)
        session.commit()

        # I got an error from sqlAlchemy, it disapeared by inserting this sleep.
        # TODO: Investigate the error.
        n += 1
        if n == 500:
            time.sleep(0.5)
            n = 0
        #session.refresh(file)
    

def get_categories_in_db():
    session = get_session()
    categories = session.exec(select(File.filetype).distinct()).all()
    return categories


def populate_categories(categories):
    console.print("[green]Populating...[/green]")
    tmp = {}
    for category in categories:
        code = settings.get_categories()[category]["code"]
        exts = settings.get_categories()[category]["ext"]
        for ext in exts:
            tmp[ext] = code
    populate_files(tmp)
    console.print("[green]Finished Populating...[/green]")


def get_hash(full_path):
    session = get_session()
    query = select(File.filehash).where(File.path == full_path)
    file_hash = session.exec(query).all()
    return file_hash[0] if file_hash else 123


def get_duplicates(full_path):
    hash = get_hash(full_path)
    session = get_session()
    query = select(File.id, File.path).where(File.filehash == hash and File.path != full_path)
    results = session.exec(query).all()
    duplicates = [(d[0], d[1]) for d in results if d[1] != full_path]  # [d for d...] doesn't work because of `d` type
    return {"hash": hash, "duplicates": duplicates}


def get_directory_contents(directory: Path):
    """Get the contents of a directory."""
    if not directory.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")

    categories_in_db = get_categories_in_db()
    extensions = []
    for cat_in_db in categories_in_db:
        extensions.extend(settings.get_extensions(cat_in_db))
    
    # List files and directories in the given directory
    items = []
    #for item in directory.iterdir():
    for item in os.scandir(directory):
        if not is_valid_file(item, extensions) and item.is_file():
            continue
        if item.name.startswith("."):
            continue
        items.append({
            "name": item.name,
            "type": "directory" if item.is_dir() else "file",
        })
    items.sort(key=lambda x: (x["type"], x["name"]))
    return items

