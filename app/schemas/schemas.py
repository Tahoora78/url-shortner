from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLCreate(BaseModel):
    original_url: HttpUrl

class URLInfo(BaseModel):
    id: int
    original_url: HttpUrl
    short_code: str
    created_at: datetime
    visit_count: int

    model_config = {
        "from_attributes": True
    }

    # class Config:
    #     orm_mode = True

class URLStats(BaseModel):
    short_code: str
    original_url: HttpUrl
    visits_count: int