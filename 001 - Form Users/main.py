from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests


templates = Jinja2Templates(directory='templates')

app = FastAPI()

app.mount("/statics_img", StaticFiles(directory="./templates/statics/images"), name='images')
app.mount("/statics_css", StaticFiles(directory="./templates/statics/css"), name='css')


#@app.post("/login", response_class=HTMLResponse)
#async def login(username: str = Form(...), password: str = Form(...), ipaddress: str = Form(...)):
#    print(username)
#    print(password)
#    print(ipaddress)
#    return {"username": username, "password": password, "ipaddress": ipaddress}

@app.post('/login')
async def login(username: str = Form(...), password: str = Form(...), public_ip: str = Form(...)):

    return {"username" : username, "password" : password, "public_ip" : public_ip}

#@app.get('/', response_class=HTMLResponse)
#def index():
#    with open("./templates/index.html", 'r') as f:
#        return HTMLResponse(content=f.read())
    
@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    public_ip = requests.get('https://checkip.amazonaws.com').text.rstrip()
    #r.json()
    #return templates.TemplateResponse('index.html', context = {'request': request, 'public_ip': public_ip})
    return templates.TemplateResponse('index.html', context = {'request': request, 'public_ip': public_ip})



