import uvicorn
from fastapi import FastAPI
from .routes import router
from . import models
from .database import engine

""" Module for launching FastAPI application """

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

# This is for Docker container. Locally use "uvicorn app.main:app --reload --port 8080 --host 0.0.0.0" (root dir)
if __name__ == "__main__":
    uvicorn.run( "main:app", host='0.0.0.0', port=8000, reload=True)