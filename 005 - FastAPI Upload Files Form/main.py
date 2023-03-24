from typing import Union
 ### dependencias : uvicorn fastapi jinja2 python-multipart python-magic python-magic-bin
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os # para poder crear carpetas
import magic

IMAGEDIR = "uploads/"
 
app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
 
@app.post('/uploadfile', response_class=HTMLResponse)
async def post_basic_form(request: Request, file: UploadFile = File(...), mail_address: str = Form(...)):
    
    carpeta_temporal = str(contador_temporal())
    carpeta_temporal = carpeta_temporal.zfill(5) + '/'

    os.mkdir('uploads/' + carpeta_temporal)
    
    print(f'Filename: {file.filename}')
      
    contents = await file.read()
      
    #save the file
    with open(f"{IMAGEDIR}{str(carpeta_temporal)}{file.filename}", "wb") as f:
        f.write(contents)
    
    size = os.stat(f"{IMAGEDIR}{str(carpeta_temporal)}{file.filename}").st_size
    if size < 1024:
        size_en_megas = "0.1 KB"
    elif size >= 1024 and size < 1048576:
        size_en_megas = str(round( size / 1024, 2)) + ' KB'
    elif size < 1048576:
        size_en_megas = "0.1 MB"
    else:
        size_en_megas = str(round(size / (1024 * 1024), 2)) + ' MB'

    file_type = magic.from_file(f"{IMAGEDIR}{str(carpeta_temporal)}{file.filename}")
    file_type_mime = magic.from_file(f"{IMAGEDIR}{str(carpeta_temporal)}{file.filename}", mime = True)
    return templates.TemplateResponse('success.html', context={'request': request, 'filename_uploaded': file.filename, 'filesize_uploaded': size,'filesize_uploaded_en_megas': size_en_megas, 'email_usuario': mail_address, 'file_type': file_type, 'file_type_mime': file_type_mime})



def contador_temporal() -> int:
    with open('.counter', 'r') as f:
        contador = f.read()
        f.close()
    
    contador = str(int(contador) + 1)

    with open(f"{'.counter'}", "w") as f:
       f.write(contador)
       f.close()

    return contador
