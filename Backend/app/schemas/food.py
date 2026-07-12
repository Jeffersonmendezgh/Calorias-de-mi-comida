from pydantic import BaseModel
from typing import List

# 1. Lo que entra desde el Frontend mediante Fetch
class FoodAnalysisRequest(BaseModel):
    texto_usuario: str

# 2. El contrato estricto que le exigiremos a Gemini (y que mapea con nuestra interfaz)
class FoodItemStructure(BaseModel):
    alimento: str
    gramos: int
    calorias_por_100g: int
    dato_educativo: str

# 3. La respuesta final que el backend le retornará al Frontend
class FoodAnalysisResponse(BaseModel):
    total_calorias: int
    desglose: List[FoodItemStructure]