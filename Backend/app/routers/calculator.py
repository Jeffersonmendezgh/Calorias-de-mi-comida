import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.food_cache import FoodCache
from app.models.text_cache import TextCache
from app.schemas.food import FoodAnalysisRequest, FoodAnalysisResponse, FoodItemStructure
from app.services.gemini_service import gemini_service

router = APIRouter(
    prefix="/calculator",
    tags=["Calculadora Nutricional"]
)


def _normalizar_texto(texto: str) -> str:
    return " ".join(texto.strip().lower().split())

@router.post("/analyze", response_model=FoodAnalysisResponse)
def analizar_plato(request: FoodAnalysisRequest, db: Session = Depends(get_db)):
    texto = request.texto_usuario
    texto_normalizado = _normalizar_texto(texto)

    #  Verificación en la Caché de Frase Completa
    texto_cacheado = db.query(TextCache).filter(TextCache.texto_original == texto_normalizado).first()
    if texto_cacheado:
        datos_cacheados = json.loads(texto_cacheado.respuesta_json)
        return FoodAnalysisResponse(
            total_calorias=datos_cacheados["total_calorias"],
            desglose=[FoodItemStructure(**item) for item in datos_cacheados["desglose"]]
        )

    #  Llamada a Gemini (Solo si la frase no existía)
    alimentos_identificados = gemini_service.analizar_texto_comida(texto)

    desglose_final = []
    total_calorias = 0
    alimentos_agregados_en_esta_sesion = set() # Evita duplicados si la IA repite un ingrediente en la misma frase

    for item in alimentos_identificados:
        alimento_key = item.alimento.strip().lower()

        alimento_en_db = db.query(FoodCache).filter(FoodCache.alimento == alimento_key).first()

        if alimento_en_db:
            calorias_base = alimento_en_db.calorias_por_100g
            dato_educativo = alimento_en_db.dato_educativo
        else:
            calorias_base = item.calorias_por_100g
            dato_educativo = item.dato_educativo

            # Solo lo agregamos a la DB si no lo pusimos ya en este mismo bucle
            if alimento_key not in alimentos_agregados_en_esta_sesion:
                nuevo_registro = FoodCache(
                    alimento=alimento_key,
                    calorias_por_100g=calorias_base,
                    dato_educativo=dato_educativo
                )
                db.add(nuevo_registro)
                alimentos_agregados_en_esta_sesion.add(alimento_key)

        #  Cálculo de calorías por regla de tres
        calorias_totales_alimento = round((calorias_base / 100) * item.gramos)
        total_calorias += calorias_totales_alimento
        
        desglose_final.append(
            FoodItemStructure(
                alimento=alimento_key, # Modificado para usar el nombre limpio y estandarizado
                gramos=item.gramos,
                calorias_por_100g=calorias_base,
                dato_educativo=dato_educativo
            )
        )

    respuesta = FoodAnalysisResponse(
        total_calorias=total_calorias,
        desglose=desglose_final
    )

    # Guardar la nueva frase en caché
    nuevo_cache_texto = TextCache(
        texto_original=texto_normalizado,
        respuesta_json=json.dumps(respuesta.model_dump())
    )
    db.add(nuevo_cache_texto)
    db.commit() 

    return respuesta

