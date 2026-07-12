from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class FoodCache(Base):
    __tablename__ = "food_cache"
    id = Column(Integer, primary_key=True, index=True)
    alimento = Column(String, unique=True, index=True, nullable=False)
    calorias_por_100g = Column(Integer, nullable=False)
    dato_educativo = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)