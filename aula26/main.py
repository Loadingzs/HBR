from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.status import HTTP_302_FOUND
import mysql.connector
import hashlib

# Configuração base
app_web = FastAPI()
app_web.add_middleware(SessionMiddleware, secret_key="sua_chave_secreta_aqui")
paginas = Jinja2Templates(directory="aula26/paginas")


# --- Funçoes auxiliares ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="1234", 
        database="escola"
    )


def requerir_login(request: Request):
    """Verifica se o usuário está logado."""
    return request.session.get("user")


# --- Rotas principais ---
@app_web.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return paginas.TemplateResponse("login.html", {"request": request})


@app_web.post("/login")
def login(request: Request, nome: str = Form(...), senha: str = Form(...)):
    hash_md5 = hashlib.md5(senha.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM ee_administracao WHERE login = %s", (nome,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    if resultado and resultado[0] == hash_md5:
        request.session["user"] = nome
        return RedirectResponse("/inicio", status_code=HTTP_302_FOUND)
    return RedirectResponse("/falha", status_code=HTTP_302_FOUND)


@app_web.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=HTTP_302_FOUND)


@app_web.get("/falha", response_class=HTMLResponse)
def falha(request: Request):
    return paginas.TemplateResponse("falha.html", {"request": request})


@app_web.get("/inicio", response_class=HTMLResponse)
def inicio(request: Request, user: str = Depends(requerir_login)):
    if not user:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)
    return paginas.TemplateResponse("inicio.html", {"request": request, "user": user})


# --- Listagens ---
@app_web.get("/alunos", response_class=HTMLResponse)
def listar_alunos(request: Request, user: str = Depends(requerir_login)):
    if not user:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM aluno")
    alunos = cursor.fetchall()
    cursor.close()
    conn.close()

    return paginas.TemplateResponse(
        "aluno.html", {"request": request, "alunos": alunos, "user": user}
    )


@app_web.get("/professores", response_class=HTMLResponse)
def listar_professores(request: Request, user: str = Depends(requerir_login)):
    if not user:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM professor")
    professores = cursor.fetchall()
    cursor.close()
    conn.close()

    return paginas.TemplateResponse(
        "professor.html", {"request": request, "professores": professores, "user": user}
    )


# --- Relatórios ---
@app_web.get("/relatorios", response_class=HTMLResponse)
def relatorios(request: Request, user: str = Depends(requerir_login)):
    if not user:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)
    return paginas.TemplateResponse("relatorio.html", {"request": request, "user": user})


@app_web.get("/relatorios/disciplinas", response_class=HTMLResponse)
def relatorio_disciplinas(request: Request, user: str = Depends(requerir_login)):
    if not user:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.id_disciplina, d.nome AS disciplina, p.nome AS professor, d.horario, -- Adicionado d.horario
               a.nome AS aluno, n.nota1, n.nota2, n.nota3, n.nota4
        FROM disciplina d
        JOIN professor p ON d.id_professor = p.id_professor
        LEFT JOIN aluno_disciplina ad ON d.id_disciplina = ad.id_disciplina
        LEFT JOIN aluno a ON ad.id_aluno = a.id_aluno
        LEFT JOIN notas n ON n.id_aluno = a.id_aluno AND n.id_disciplina = d.id_disciplina
        ORDER BY d.nome, a.nome;
    """)
    registros = cursor.fetchall()
    cursor.close()
    conn.close()

    # Agrupar por disciplina
    disciplinas = {}
    for r in registros:
        disc = disciplinas.setdefault(r["id_disciplina"], {
            "disciplina": r["disciplina"],
            "professor": r["professor"],
            "horario": r["horario"], # Adicionado 'horario' ao objeto
            "alunos": []
        })
        if r["aluno"]:
            disc["alunos"].append({
                "aluno": r["aluno"],
                "nota1": r["nota1"],
                "nota2": r["nota2"],
                "nota3": r["nota3"],
                "nota4": r["nota4"]
            })

    disciplinas_lista = list(disciplinas.values())

    return paginas.TemplateResponse(
        "relatorio_disciplinas.html",
        {"request": request, "user": user, "disciplinas": disciplinas_lista}
    )

@app_web.get("/relatorios/alunos", response_class=HTMLResponse)
def relatorio_alunos(request: Request, user: str = Depends(requerir_login)):
    if not user:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id_aluno, a.nome AS aluno, d.nome AS disciplina,
               n.nota1, n.nota2, n.nota3, n.nota4
        FROM aluno a
        LEFT JOIN aluno_disciplina ad ON a.id_aluno = ad.id_aluno
        LEFT JOIN disciplina d ON ad.id_disciplina = d.id_disciplina
        LEFT JOIN notas n ON n.id_aluno = a.id_aluno AND n.id_disciplina = d.id_disciplina
        ORDER BY a.nome, d.nome;
    """)
    registros = cursor.fetchall()
    cursor.close()
    conn.close()

    # Agrupar por aluno
    alunos = {}
    for r in registros:
        aluno = alunos.setdefault(r["id_aluno"], {
            "aluno": r["aluno"],
            "disciplinas": []
        })
        if r["disciplina"]:
            notas = [r["nota1"], r["nota2"], r["nota3"], r["nota4"]]
            notas_validas = [n for n in notas if n is not None]
            
            # Garante que a média só é calculada se houver notas válidas
            media = round(sum(notas_validas) / len(notas_validas), 2) if notas_validas else None
            
            status = (
                "Aprovado" if media is not None and media >= 6
                else "Reprovado" if media is not None 
                else "-"
            )
            
            aluno["disciplinas"].append({
                "disciplina": r["disciplina"],
                "nota1": r["nota1"],
                "nota2": r["nota2"],
                "nota3": r["nota3"],
                "nota4": r["nota4"],
                "media": media,
                "status": status
            })

    alunos_lista = list(alunos.values())

    return paginas.TemplateResponse(
        "relatorio_alunos2.html",
        {"request": request, "user": user, "alunos": alunos_lista} # Passando a lista corrigida
    )