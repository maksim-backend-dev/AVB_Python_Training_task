from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from schemas import URLRequest
import uuid
import httpx

""" Module for an endpoints """

router = APIRouter()

# Global storage made for a simple testing
url_store = {}

@router.post("/", status_code=201)
async def shorten_url(data: URLRequest):
    """
    Receives a URL and returns shortened version of it
    Checking for duplicates (optional)
    """
    for short_id, original_url in url_store.items():
        if original_url == data.url:
            return {"shorten_url": f"http://127.0.0.1:8000/{short_id}"}

    short_id = str(uuid.uuid4())[:6]
    url_store[short_id] = data.url
    return {"shorten_url": f"http://127.0.0.1:8000/{short_id}"}

@router.get("/{short_id}")
async def redirect(short_id: str):
    """
    Receives shortened URL and redirects to an original URL
    """
    original_url = url_store.get(short_id)

    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(original_url, status_code=307)

@router.get("/test/external-data")
async def fetch_external_data():
    """
    Fetches an external data. This is a simple version.
    :return:
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.agify.io?name=alice")

    return response.json()