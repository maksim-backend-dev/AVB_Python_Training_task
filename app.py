from fastapi import FastAPI
from routes import router
"""
Initializing the FastAPI application and connecting routes.
"""
app = FastAPI()
app.include_router(router)