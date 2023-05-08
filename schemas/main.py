from pydantic import BaseModel

class GetNewsParams(BaseModel):
    page: int

class GetNewsReponse(BaseModel):
    title: str
    url: str
    by: str
    type: str
    score: int
    time: int