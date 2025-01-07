from fastapi import FastAPI
from fastapi.responses import FileResponse


front_app = FastAPI()

@front_app.get("/")
async def read_index():
    return FileResponse('./frontend/ui/index.html')
