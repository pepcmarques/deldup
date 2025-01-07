import uvicorn
import multiprocessing

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db import init_db, populate_db

from frontend.frontend import front_app
from backend.backend import api_app


init_db()
populate_db()


app = FastAPI()


app.mount('/api/', api_app)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount('/', front_app)


if __name__ == '__main__':
    multiprocessing.freeze_support()  # For Windows support
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)
