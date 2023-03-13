from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/statics_img", StaticFiles(directory="./templates/statics/images"), name='images')
app.mount("/statics_css", StaticFiles(directory="./templates/statics/css"), name='css')


@app.post("/login", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...), ipaddress: str = Form(...)):
    print(username)
    print(password)
    print(ipaddress)
    return {"username": username, "password": password, "ipaddress": ipaddress}

@app.get('/', response_class=HTMLResponse)
def index():
    with open("./templates/index.html", 'r') as f:
        return HTMLResponse(content=f.read())