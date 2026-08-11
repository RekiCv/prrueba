from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()

templates = Jinja2Templates(directory="templates")

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

@app.get("/")
def leer_notas(request: Request):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notas")
    notas = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse(request, "index.html", {"notas": notas})

@app.post("/agregar")
def agregar_nota(contenido: str = Form(...)):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notas (contenido) VALUES (?)", (contenido,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)