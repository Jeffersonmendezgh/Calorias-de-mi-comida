import json
from google import genai
from google.genai import types
from app.config import settings
from app.schemas.food import FoodItemStructure
from typing import List

class GeminiService:
    def __init__(self):
        """
        Inicializa el cliente de Google GenAI usando la API Key del .env
        """
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = "gemini-2.5-flash"

    def analizar_texto_comida(self, texto_usuario: str) -> List[FoodItemStructure]:
        """
        Envía la frase libre del usuario a Gemini y devuelve la lista estructurada de alimentos.
        """
        system_instruction = (
            "Eres un nutricionista experto y un backend de software de alta precisión.\n"
            "Tu tarea es identificar cada alimento mencionado por el usuario y estimar sus "
            "calorías estrictamente basadas en estándares internacionales como la base de datos de la USDA.\n"
            "Debes calcular y extraer:\n"
            "1. El nombre del alimento en minúsculas y limpio (ej: 'papa cocida', 'pechuga de pollo').\n"
            "2. Los gramos exactos aproximados que el usuario consumió.\n"
            "3. Las calorías estándar que tiene ese alimento POR CADA 100 GRAMOS.\n"
            "4. Una breve descripción nutricional de valor sobre el alimento para fines de SEO y AdSense.\n\n"
            "REGLA CRÍTICA: Si el usuario no especifica los gramos de un alimento, estima una porción "
            "estándar normal (ej: una manzana promedio son 150g). Si el texto es incoherente o no contiene "
            "alimentos, devuelve una lista vacía."
        )

        try:
            esquema_objeto = FoodItemStructure.model_json_schema()
            esquema_objeto.pop("title", None)
            if "properties" in esquema_objeto:
                for prop in esquema_objeto["properties"].values():
                    prop.pop("title", None)

            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema={
                    "type": "ARRAY",
                    "items": esquema_objeto
                },
                temperature=0.2
            )

            # Hacemos la llamada a Google Gemini
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=texto_usuario,
                config=config
            )

            if not response.text:
                return []
                
            datos_json = json.loads(response.text)
            
            # Mapeamos los diccionarios crudos del JSON de vuelta a objetos Pydantic validados
            return [FoodItemStructure(**item) for item in datos_json]

        except Exception as e:
            print(f"[Error en GeminiService]: {e}")
            return []
# Instanciamos el servicio como un Singleton para reutilizarlo en los controladores
gemini_service = GeminiService()