from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Extraemos la URL de la base de datos desde nuestra configuración segura
DATABASE_URL = settings.DATABASE_URL

# Para SQLite, necesitamos el argumento 'check_same_thread': False
# Esto permite que FastAPI use múltiples hilos de ejecución de manera segura
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Creamos una fábrica de sesiones independientes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta será la clase base de la cual heredarán todos nuestros modelos de SQLAlchemy
Base = declarative_base()

# Una función auxiliar (Dependency Injection) para manejar las sesiones por cada petición HTTP
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()