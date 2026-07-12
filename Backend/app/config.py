from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # Definimos las variables y sus tipos de datos esperados
    PROJECT_NAME: str = "Calorias de mi comida"
    DEBUG: bool = False
    DATABASE_URL: str
    GEMINI_API_KEY: str

    # Configuramos Pydantic para que busque el archivo .env una carpeta atrás (en la raíz)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # Ignora otras variables que no hayamos definido aquí
    )

# Instanciamos la configuración para importarla en el resto del proyecto
settings = Settings()