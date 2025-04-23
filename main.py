import uvicorn
from app import app
"""
Entry point to the application. Starts the FastAPI server via Uvicorn.
"""
if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)