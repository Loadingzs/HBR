from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

app_web = FastAPI()
paginas = Jinja2Templates(directory='HBR/paginas')

#acrescentando um comentário para atualizar o GitHub

@app_web.get('/')
async def index(request: Request):
    context = {
        "request": request,
        "resultado": 0
    }
    return paginas.TemplateResponse('calculadora.html', context)

