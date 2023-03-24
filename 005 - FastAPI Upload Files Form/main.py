# API con formulario para subir ficheros a un servidor
# Lanzar la API> uvicorn main:app --reload
# Dependencias : uvicorn fastapi jinja2 python-multipart python-magic python-magic-bin

# De FastAPI usaremos FastAPI (la propia API), Request (para poder manejar las respuestas de la API),
#  UpLoadFile y File (para poder trabajar con elos objetos del tipo ficheros para subida) y
#   Form (para poder trabajar con los formularios desde la API)
from fastapi import FastAPI, Request, UploadFile, File, Form

# Con fastapi.response y fastapi.templating, podemos gestionar ell envío y manipulación de ficheros HTML
#  desde la API
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Con fastapi.staticfile podemos crear rutas estáticas a las que acceder desde los HTML para poder mostrar
#  recursos estáticos en los HTML como .gif, .jpg, .css, ...
from fastapi.staticfiles import StaticFiles

import os  # para poder crear carpetas
import magic  # para información sobre el tipo de fichero

UPLOADS_DIR = "uploads/" # Definimos el directorio donde guardaremos los ficheros subidos

# Definimos la API en la variable 'app'
app = FastAPI()
# Definimos el directorio donde están los HTML
templates = Jinja2Templates(directory="templates")

# Montamos una carpeta estática para almacenar los recursos para los HTML (gif, jpg, ico, css, ...)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Definimos que al llamar a 127.0.0.1:8000/, nuestra API realizará esta acción, definida con la función 'home'
# La función 'home' no es ASYNC, pues es un get al que no hay que esperar, se llama y listo
# Lo que devuelve esta función, es el propio fichero 'index.html' como respuesta. Dentro de index.html se invoca
# a base.html, que contiene la cabecera de la web mostrada e index.html el cuerpo
@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/uploadfile', response_class=HTMLResponse)
async def post_basic_form(request: Request, file: UploadFile = File(...), mail_address: str = Form(...)):
    carpeta_temporal = contador_temporal()
    carpeta_temporal = carpeta_temporal.zfill(5) + '/'

    os.mkdir('uploads/' + carpeta_temporal)

    print(f'Filename: {file.filename}')

    contents = await file.read()

    # save the file
    with open(f"{UPLOADS_DIR}{str(carpeta_temporal)}{file.filename}", "wb") as f:
        f.write(contents)

    size = os.stat(f"{UPLOADS_DIR}{str(carpeta_temporal)}{file.filename}").st_size
    if size < 1024:
        size_en_megas = "0.1 KB"
    elif (size >= 1024) and (size < 1048576):
        size_en_megas = str(round(size / 1024, 2)) + ' KB'
    elif size < 1048576:
        size_en_megas = "0.1 MB"
    else:
        size_en_megas = str(round(size / (1024 * 1024), 2)) + ' MB'

    file_type = magic.from_file(f"{UPLOADS_DIR}{str(carpeta_temporal)}{file.filename}")
    file_type_mime = magic.from_file(f"{UPLOADS_DIR}{str(carpeta_temporal)}{file.filename}", mime=True)
    return templates.TemplateResponse('success.html', context={'request': request,
                                                               'file_name_uploaded': file.filename,
                                                               'file_size_uploaded': size,
                                                               'file_size_uploaded_en_megas': size_en_megas,
                                                               'email_usuario': mail_address,
                                                               'file_type': file_type,
                                                               'file_type_mime': file_type_mime})


def contador_temporal() -> str:
    with open('.counter', 'r') as f:
        contador = f.read()
        f.close()

    contador = str(int(contador) + 1)

    with open(f"{'.counter'}", "w") as f:
        f.write(contador)
        f.close()

    return contador
