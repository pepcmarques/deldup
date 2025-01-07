from sqlmodel import SQLModel, Field
from pydantic import BaseModel


# --- FILES ---

class FileBase(SQLModel):
    name: str
    path: str
    filetype: str
    fileext: str
    filehash: str
    #year: Optional[int] = None


class File(FileBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class FileCreate(FileBase):
    pass


class FileDelete(BaseModel):
    filePath: str
