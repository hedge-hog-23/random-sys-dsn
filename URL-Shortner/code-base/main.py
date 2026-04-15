from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from models import URLRequest, URLResponse
from utils import generate_short_url
from storage import url_store

app = FastAPI()
BASE_URL = "http://localhost:8000/"

@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest) -> URLResponse:
    short_code = generate_short_url()
    url_store[short_code] = str(request.long_url)

    short_url = f"{BASE_URL}{short_code}"
    return URLResponse(short_url=short_url)

@app.get("/{short_code}")
def redirect_to_long_url(short_code: str):
    long_url = url_store.get(short_code)
    if long_url:
        # return {"long_url": long_url}
        return RedirectResponse(url=long_url)
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")
