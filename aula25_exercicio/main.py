from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
import hashlib
from starlette.responses import Response
from starlette.status import HTTP_302_FOUND
from starlette.middleware.sessions import SessionMiddleware

app_web = FastAPI()
app_web.add_middleware(SessionMiddleware, secret_key="sua_chave_secreta_aqui")
paginas = Jinja2Templates(directory="paginas")


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ifsp",
        database="aula25"
    )


@app_web.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return paginas.TemplateResponse("login.html", {"request": request})

@app_web.post("/login")
def login(
    Request: Request,
    response: Response,
    nome: str = Form(...),
    senha: str = Form(...),
):
    conn = get_db_connection()
    cursor = conn.cursor()
    hash_password = hashlib.md5(senha.encode()).hexdigest()
    cursor.execute("SELECT password FROM tb_administracao WHERE login = %s", (nome,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result and result[0] == hash_password:
        Request.session['user'] = nome
        return RedirectResponse("/sucesso", status_code=HTTP_302_FOUND)
    else:
        return RedirectResponse("/falha", status_code=HTTP_302_FOUND)




@app_web.get("/sucesso", response_class=HTMLResponse)
def success(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)
    return paginas.TemplateResponse("sucesso.html", {"request": request, "user": user})

@app_web.get("/falha", response_class=HTMLResponse)
def fail(request: Request):
    return paginas.TemplateResponse("falha.html", {"request": request})