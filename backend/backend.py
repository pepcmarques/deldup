import os
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse

from sqlalchemy import delete
from sqlmodel import select

from sqlmodel.ext.asyncio.session import AsyncSession

from app.dbengine import get_session
from app.models import File, FileCreate, FileDelete

from pathlib import Path

from services import get_directory_contents, get_duplicates, get_hash
import settings


api_app = FastAPI()


@api_app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@api_app.get("/files", response_model=list[File])
async def get_files(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(File))
    images = result.scalars().all()
    return [File(name=image.name, path=image.path, img_type=image.img_type, id=image.id) for image in images]


@api_app.post("/files")
async def add_file(file: FileCreate, session: AsyncSession = Depends(get_session)):
    file = File(name=file.name, path=file.path, img_type=file.filetype)
    session.add(file)
    await session.commit()
    await session.refresh(file)
    return file



@api_app.get("/directoryTree")
async def directory_tree(path: str = "", level: int = 0):
    """
    API Endpoint to fetch the contents of a directory.
    :param path: Relative path from the root directory.
    :return: List of files and directories in the specified path.
    """
    target_dir = Path(path)
    try:
        contents = get_directory_contents(target_dir)
        return {"path": path, "children": contents, "level": level + 1}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@api_app.get("/findDuplicate")
async def find_duplicates(path: str = ""):
    """
    API Endpoint to fetch the duplicates of a file.
    :param path: Relative path from the root directory.
    :return: List of files with the same hash.
    """
    try:
        duplicates = get_duplicates(path)
        return duplicates
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@api_app.get("/getFile")
async def get_file(path: str):
    """Serve the requested file."""
    file = Path(path)
    if not file.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file)


@api_app.delete("/deleteFile/{fileId}", status_code=204)
async def delete_file(fileId: int, fileDelete: FileDelete):
    """Delete file"""
    filePath = Path(fileDelete.model_dump().get("filePath", "/path/to/anywhere/that/doesnt/exist"))

    # Remove entry from DB
    mode = settings.get_mode()
    if mode == "db" or mode == "all":
        session = get_session()
        session.exec(delete(File).where(File.id == int(fileId)))
        print("Deleting from DB")
        print(f"  - delete entry {fileId} from database")
        session.commit()

    # Delete file from filesystem
    if mode == "fs" or mode == "all":
        print("Deleting from FS")
        print(f"  - delete {filePath} from disk")
        filePath.unlink(missing_ok=True)
    
    return {"ok": True}


@api_app.get("/home")
async def home():
    return {"baseDir": settings.get_home_dir()}
