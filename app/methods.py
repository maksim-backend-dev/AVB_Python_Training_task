from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from .schemas import URLRequest
from sqlalchemy.orm import Session
from .models import URLS
import uuid
import httpx


def method_shortening_url(data: URLRequest, db: Session):

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


def method_redirecting_url(short_id: str, db: Session):

    result = db.query(URLS).filter(URLS.shortened_url == short_id).first()

    if not result:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(result.original_url, status_code=307)


async def method_fetching_external_data():

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.agify.io?name=alice")

    return response.json()