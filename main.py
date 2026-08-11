import sqlite3
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_db():
    return sqlite3.connect("database.db")

# 1. Ruta principal: Carga la lista de notas
@app.get("/")
def leer_home(request: Request):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, contenido FROM notas")
    notas = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse(request=request, name="index.html", context={"notas": notas})

# 2. Ruta para agregar notas
@app.post("/agregar")
def agregar_nota(contenido: str = Form(...)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notas (contenido) VALUES (?)", (contenido,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

# 3. Ruta para eliminar notas (esta es la que faltaba)
@app.post("/eliminar/{nota_id}")
def eliminar_nota(nota_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notas WHERE id = ?", (nota_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)