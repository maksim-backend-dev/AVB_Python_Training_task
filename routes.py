from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from database import get_db
from schemas import URLRequest
from sqlalchemy.orm import Session
from models import URLS
import uuid
import httpx


""" Module for an endpoints """

router = APIRouter()

@router.post("/", status_code=201)
async def shorten_url(data: URLRequest, db: Session = Depends(get_db)):
    """
    Receives a URL and returns shortened version of it
    Checking for duplicates
    """
    """ The port 8080 is for a docker purposes """
    existing = db.query(URLS).filter(URLS.original_url == data.url).first()
    if existing:
        return {"shorten_url": f"http://127.0.0.1:8080/{existing.shortened_url}"}

    short_id = str(uuid.uuid4())[:6]
    new_entry = URLS(shortened_url=short_id, original_url=data.url)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"shorten_url": f"http://127.0.0.1:8080/{short_id}"}

@router.get("/{short_id}")
async def redirect(short_id: str, db: Session = Depends(get_db)):
    """
    Receives shortened URL and redirects to an original URL
    """
    result = db.query(URLS).filter(URLS.shortened_url == short_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(result.original_url, status_code=307)

@router.get("/test/external-data")
async def fetch_external_data():
    """
    Fetches an external data. This is a simple version.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.agify.io?name=alice")

    return response.json()