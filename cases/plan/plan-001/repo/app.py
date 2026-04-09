"""Shrink — URL shortener API."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from storage import URLStore

app = FastAPI(title="Shrink", version="0.1.0")
store = URLStore()


class ShortenRequest(BaseModel):
    url: str


@app.post("/shorten")
def shorten(req: ShortenRequest):
    code = store.create(req.url)
    return {"short": code, "url": f"http://localhost:8000/{code}"}


@app.get("/{code}")
def redirect(code: str):
    url = store.get(code)
    if url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=url)


@app.delete("/{code}")
def delete(code: str):
    if not store.delete(code):
        raise HTTPException(status_code=404, detail="Short URL not found")
    return {"status": "deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
