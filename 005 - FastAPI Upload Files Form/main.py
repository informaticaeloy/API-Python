#uploadajax/main.py
from typing import Union
 
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import time # para usar time.sleep(seconds)
import os # para poder crear carpetas
from datetime import date # para la creación de la carpeta temporal

IMAGEDIR = "uploads/"
 
app = FastAPI()
templates = Jinja2Templates(directory="templates")
 
@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
 
@app.post('/uploadfile', response_class=HTMLResponse)
async def post_basic_form(request: Request, file: UploadFile = File(...)):
    
    carpeta_temporal = str(contador_temporal())
    carpeta_temporal = carpeta_temporal.zfill(5) + '/'

    os.mkdir('uploads/' + carpeta_temporal)
    
    print(f'Filename: {file.filename}')
      
    contents = await file.read()
      
    #save the file
    with open(f"{IMAGEDIR}{str(carpeta_temporal)}{file.filename}", "wb") as f:
        f.write(contents)
    
    return templates.TemplateResponse('success.html', context={'request': request})



def contador_temporal() -> int:
    with open('.counter', 'r') as f:
        contador = f.read()
        f.close()
    
    contador = str(int(contador) + 1)

    with open(f"{'.counter'}", "w") as f:
       f.write(contador)
       f.close()

    return contador