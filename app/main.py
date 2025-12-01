from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse

from .schemas import schemas
from .models import models
from .crud import crud
from .database import engine
import uvicorn
from .utils.logging import log_visit
from .increment_runner import visit_queue

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener Task")

@app.post("/shorten", response_model=schemas.URLInfo, status_code=201)
def shorten(url_in: schemas.URLCreate) -> schemas.URLInfo:
    url = crud.create_short_url(str(url_in.original_url))
    return schemas.URLInfo.from_orm(url)

@app.get("/{short_code}")
@log_visit
def redirect(short_code: str, request: Request):
    url = crud.get_url_by_code(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="Short code not found")
    # increment visit count in queue. it should add the shortcode to the queue
    visit_queue.put(short_code)
    return RedirectResponse(url.original_url)

@app.get("/stats/{short_code}")
def stats(short_code: str) -> schemas.URLStats:
    url = crud.get_url_by_code(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="Short code not found")
    count = crud.get_visit_count(short_code)
    return schemas.URLStats(
        short_code=short_code,
        original_url=url.original_url,
        visits_count=count
    )


if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
