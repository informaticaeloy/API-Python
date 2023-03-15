from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

templates = Jinja2Templates(directory='templates')

app = FastAPI()

app.mount("/statics_img", StaticFiles(directory="./templates/statics/images"), name='images')
app.mount("/statics_css", StaticFiles(directory="./templates/statics/css"), name='css')

@app.post('/login')
async def login(username: str = Form(...), password: str = Form(...), public_ip: str = Form(...)):
    datos_login = {"username" : username, "password" : password, "public_ip" : public_ip}
    return datos_login
    

@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    public_ip = requests.get('https://checkip.amazonaws.com').text.rstrip()
    return templates.TemplateResponse('index.html', context = {'request': request, 'public_ip': public_ip})



