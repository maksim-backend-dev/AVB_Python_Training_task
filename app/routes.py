from fastapi import APIRouter, Depends
from .database import get_db
from .methods import *



""" Module for an endpoints """

router = APIRouter()

@router.post("/", status_code=201)
async def shorten_url(data: URLRequest, db: Session = Depends(get_db)):

    """
    Receives a URL and returns shortened version of it
    Checking for duplicates
    """

    return method_shortening_url(data, db)

@router.get("/{short_id}")
async def redirect(short_id: str, db: Session = Depends(get_db)):

    """ Receives shortened URL and redirects to an original URL """

    return method_redirecting_url(short_id, db)


@router.get("/test/external-data")
async def fetch_external_data():

    """
    Fetches an external data. This is a simple version.
    """

    return await method_fetching_external_data()