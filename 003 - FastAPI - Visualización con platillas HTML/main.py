from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import dotenv_values
from fastapi import APIRouter, Body, Request, Response, HTTPException, status, FastAPI
from fastapi.encoders import jsonable_encoder
from typing import List
from json2html import *
from models import Book, BookUpdate
import json
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
from fastapi.staticfiles import StaticFiles

config = dotenv_values(".env")

app = FastAPI()
router = APIRouter()

class Recipe(BaseModel):
    id: str
    st: str
    
TEMPLATES = Jinja2Templates(directory=str("templates"))
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_description="List all books", response_model=List[Book])
def list_books(request: Request):
    books = collection.find(limit=10)
    lista_de_books = []
    for book in books:
        book_actual = {"_id":str(book["_id"]), "st": str(book["st"])}
        lista_de_books.append(book_actual)
        #json.dumps(lista_de_books)
    print(type(lista_de_books))

mongodb_client = MongoClient(config["ATLAS_URI"])
database = mongodb_client[config["DB_NAME"]]
collection = database[config["COLLECTION"]]
    
    print(type(lista_de_books))
    return TEMPLATES.TemplateResponse("index.html",{"request": request, "recipes": lista_de_books})

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
