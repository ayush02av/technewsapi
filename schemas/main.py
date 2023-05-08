from pydantic import BaseModel
from typing import Optional

class GetNewsParams(BaseModel):
    page: int

class GetNewsReponse(BaseModel):
    title: Optional[str]
    url: Optional[str]
    by: Optional[str]
    type: Optional[str]
    score: Optional[int]
    time: Optional[int]