import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from fastapi.responses import RedirectResponse
import httpx

url_store = {} #short_id: original_url
app = FastAPI()

class URLRequest(BaseModel):
    url: str

# 1. Get an abbreviated version of the transmitted URL - using uuid to generate short_id. In addition I made a
# duplicate check
@app.post("/", status_code=201)
def shorten_url(data: URLRequest):
    for short_id, original_url in url_store.items():
        if original_url == data.url:
            return {"shorten_url:": f"http://127.0.0.1:8000/{short_id}"}

    short_id = str(uuid.uuid4())[:6]
    url_store[short_id] = data.url
    return {"shorten_url:": f"http://127.0.0.1:8000/{short_id}"}


# 2. Return the original URL.
@app.get("/{short_id}")
def redirect(short_id: str):
    original_url = url_store.get(short_id)
    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(original_url, status_code=307)


# 3. Make an async service request and return the data - as there was not much more description of what to do,
# I decided to make something simple.
@app.get("/test/external-data")
async def fetch_external_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.agify.io?name=alice")
    return response.json()


# To run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True,workers=3)