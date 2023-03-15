# Formulario simple de login

### Este formulario simple de login recoge la IP pública del usuario de https://checkip.amazonaws.com/ y pasa los campos 'username', 'password' e 'ipaddress' mediante POST a la API (FastAPI) de Python que trabaja con esos datos.

### Explicación:

```python
from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

# Declaramos el directorio de los 'templates', donde guardaremos los HTML que usaremos como plantillas
templates = Jinja2Templates(directory='templates')

app = FastAPI()

# Montamos estas rutas estáticas para poder acceder a los recursos (css, imgs, ico, ...)
app.mount("/statics_img", StaticFiles(directory="./templates/statics/images"), name='images')
app.mount("/statics_css", StaticFiles(directory="./templates/statics/css"), name='css')

# Definimos una función que será llamada al acceder a 'URL'+'/'
# En primer ligar lo definimos como método 'GET', obtenemos la IP pública y 'creamos' el HTML con
#  'TemplateResponse' de Jinja2Templates. Lo que hace es presentar el HTML, al que le pasamos el valor de
#   la IP pública (como argumento) con :                    *************************\/\/\/\/\/\/\/\/\/\/\/
#    return templates.TemplateResponse('index.html', context = {'request': request, 'public_ip': public_ip})
#     podremos invovar al valor de esta variable dentro del código HTML con {{ public_ip }}. Cada vez que en el HTML aparezca
#      la cadena {{ public_ip }}, esta será sustituida por el valor de la variable
#       y el request para que el HTML nos pueda devolver valores con: ***** \/\/\/\/\/
#        return templates.TemplateResponse('index.html', context = {'request': request, 'public_ip': public_ip})
@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    public_ip = requests.get('https://checkip.amazonaws.com').text.rstrip()
    return templates.TemplateResponse('index.html', context = {'request': request, 'public_ip': public_ip})

# El HTML tiene un formulario con 3 campos INPUT, cuyos names son username, password y public_ip (este está oculto), que se definen
#  como variable en esta función y se asigna la característica '= Form(...), para indicar que será 'rellenados' desde el formulario
#   y con (...) indicamos que es obligatorio. El formulario se define en el HTML como
#    <form id="submitForm" action="/login" method="POST" enctype="multipart/form-data">
#     donde 'action' es el nombre de la URL a visitar cuando se pula el botón, con lo que llamará a esta función, y las características
#      han de ser method="POST" , igual que la definición de la función y el enctype="multipart/form-data" para que entienda
#       la codificación del paquete HTTP con POST
@app.post('/login')
async def login(username: str = Form(...), password: str = Form(...), public_ip: str = Form(...)):
    datos_login = {"username" : username, "password" : password, "public_ip" : public_ip}
    return datos_login
```
