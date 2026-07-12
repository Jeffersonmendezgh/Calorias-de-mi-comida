from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import calculator as calculator_router
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# 1. Creamos las tablas en la Base de Datos automáticamente.
# Al arrancar, SQLAlchemy busca todos los modelos (como FoodCache) 
# y crea las tablas en el archivo 'nutri_ia.db' si aún no existen.
Base.metadata.create_all(bind=engine)



# 2. Inicializamos la aplicación de FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    description="Backend inteligente con IA para el calculo de calorias por comidas"
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
#ruta absoluta frontend
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "Frontend")

#rutas especificas
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")


#montar static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción aquí pondrás la URL real de tu página web (ej: https://midominio.com)
    allow_credentials=True,
    allow_methods=["*"], # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"], # Permite enviar cualquier cabecera (headers)
)



@app.get("/")
def read_root():
    return {
        "status": "online",
        "proyecto": settings.PROJECT_NAME,
        "documentacion_automatica": "/docs"
    }

@app.get("/calculator/", response_class=HTMLResponse)
async def calculator(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request":request})

app.include_router(calculator_router.router)