import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Book(BaseModel):
    id: str #= Field(default_factory=uuid.uuid4, alias="_id")
    st: str #= Field(...)
    

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "5553a998e4b02cf7151190bc",
                "st": "x+66300-025200",
            }
        }

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    synopsis: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "Don Quixote is a Spanish novel by Miguel de Cervantes..."
            }
        }