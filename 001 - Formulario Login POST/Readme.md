# Formulario simple de login

### Este formulario simple de login recoge la IP pública del usuario de https://checkip.amazonaws.com/ y pasa los campos 'username', 'password' e 'ipaddress' mediante POST a la API (FastAPI) de Python que trabaja con esos datos.

### Explicación:

#### Código de main.py

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

#### Y este es el código de index.html

```html
<!DOCTYPE html>
<html lang='es' >
<head>
    <meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />
    <!--
        á -> &aacute;
        é -> &eacute;
        í -> &iacute;
        ó -> &oacute;
        ú -> &uacute;
        ñ -> &ntilde;
    -->

    <title>Password Reset</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" 
          rel="stylesheet" 
          integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
          crossorigin="anonymous">
    <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Muli'>
    <link rel="stylesheet" href="./statics_css/style.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    
</head>

<body>
    <div class="pt-5">
        <h1 class="text-center">Password reset</h1>
  
        <div class="container">
            <div class="row">
                <div class="col-md-5 mx-auto">
                    <div class="card card-body">
                                                    
                        <form id="submitForm" action="/login" method="POST" enctype="multipart/form-data">
                            <div class="imgcontainer">
                                <img src="./statics_img/img_avatar.png" alt="Avatar" class="avatar">
                            </div>    
			    <div class="form-group required">
                                <lSabel >Username / Email</lSabel>
                                <input type="text" class="form-control text-lowercase" id="username" required="" name="username" value="">
                            </div>                    
                                
                            <div class="form-group required">
    			        <lSabel >Password</lSabel>
                                <input type="text" class="form-control text-lowercase" id="password" required="" name="password" value="">
		    	    </div>
				
                            <div class="form-group required">
                                <lSabel for="getipaddress">La IP de origen quedar&aacute registrada:</lSabel>
                                <b><span class=ipaddress id="ipaddress" name="public_ip" value="{{ public_ip }}">{{ public_ip }}</b>
                                <input type="text" class="form-control text-lowercase" id="public_ip" hidden name="public_ip" value="{{ public_ip }}">
                            </div>
                            
                            <div class="form-group pt-1">
                                <button class="btn btn-primary btn-block" type="submit" value="Submit">Enviar</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

#### Estructura de directorios

<kbd>![image](https://user-images.githubusercontent.com/20743678/225244172-bd8d6201-043c-44ec-9ac4-f07c28baaa4a.png)</kbd>

#### Llamada al server

La llamada al server se hace de la siguiente forma, en una terminal en mi caso dentro de VS Code. main se refiere al fichero .py a llamar y app el nombre declarado de la aplicación de FastAPI dentro del .py

Con la opción --reload, nos reiniciará el server cada vez que modifiquemos un fichero de código sin tener que pararlo y arrancarlo de nuevo

```python
python -m uvicorn  main:app --reload
```

#### Llamada al server (alternativa)

Podemos lanzar nuestro servidor con el comando anterior desde la terminal, o podemos crear un fichero que haga esa llamada. He creado una prueba en el fichero \_\_main\_\_.py , que podemos ejecutar aparte.

```python
# Importamos las librerías necesarias
from uvicorn import Config, Server

# Definimos la configuración del server
server = Server(
    Config(
        "main:app",       # Nombre del fichero y nombre de la aplicación a lanzar, del tipo fichero:applicación
        host="127.0.0.1", # Url desde donde nuestro server será accesible. 127.0.0.1 sólo para nuestra máquina, 0.0.0.0 para cualquier equipo de la red
        port=9002,        # Puerto de escucha de nuestro server. Si no se especifica, por defecto es el 8000
        reload=True,      # La opción de reload es para que se reinicia cada vez que un fichero es modificado
        log_level='debug' # Options: 'critical', 'error', 'warning', 'info', 'debug', 'trace'
    ),
 )
server.run()

```

#### Aspecto final
<kbd>![image](https://user-images.githubusercontent.com/20743678/225308479-4a918499-5b9b-47f2-adbc-c3b1c5d52d5d.png)</kbd>
