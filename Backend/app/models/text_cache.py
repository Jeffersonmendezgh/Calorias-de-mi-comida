from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class TextCache(Base):
    __tablename__ = "text_cache"

    id = Column(Integer, primary_key=True, index=True)
    texto_original = Column(String, unique=True, index=True, nullable=False)
    respuesta_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)