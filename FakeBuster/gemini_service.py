"""
Servicio de análisis de noticias usando Gemini AI.

Utiliza la API oficial de Google para analizar la credibilidad
de noticias basado en coherencia, contexto histórico y señales de desinformación.
"""

import logging
import os

from dotenv import load_dotenv
from google import genai

from .constants import (
    ERROR_ANALIZAR_NOTICIA,
    ERROR_SIN_API_KEY,
    ERROR_SIN_RESPUESTA_VALIDA,
    MODELO_GEMINI,
    PROMPT_ANALISIS_NOTICIA,
)

logger = logging.getLogger(__name__)

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = None

if GOOGLE_API_KEY:
    client = genai.Client(api_key=GOOGLE_API_KEY)
    logger.info("API de Gemini configurada correctamente")
else:
    logger.warning("GOOGLE_API_KEY no configurada")

"...."
def _nombre_seguro(valor):
    """Obtiene el nombre de un enum u objeto sin registrar su contenido completo."""
    if valor is None:
        return None
    return getattr(valor, "name", None) or str(valor).split(".")[-1]


def _obtener_codigo_status(error):
    """Busca códigos HTTP comunes en excepciones de clientes API."""
    for objeto in (
        error,
        getattr(error, "response", None),
        getattr(error, "http_response", None),
    ):
        for atributo in ("status_code", "status", "code"):
            codigo = getattr(objeto, atributo, None)
            if isinstance(codigo, int):
                return codigo
    return None


def _clasificar_error(codigo):
    """Clasifica errores HTTP sin exponer detalles de la solicitud."""
    if codigo == 429 or codigo is not None and 500 <= codigo <= 599:
        return "transitorio"
    if codigo is not None and 400 <= codigo <= 499:
        return "permanente"
    return "desconocido"


def _registrar_diagnostico_respuesta(response):
    """Registra metadatos seguros cuando Gemini no devuelve texto usable."""
    prompt_feedback = getattr(response, "prompt_feedback", None)
    block_reason = _nombre_seguro(getattr(prompt_feedback, "block_reason", None))
    candidates = getattr(response, "candidates", None)

    if not candidates:
        logger.warning(
            "Respuesta de Gemini sin candidatos; prompt_feedback_disponible=%s "
            "block_reason=%s",
            prompt_feedback is not None,
            block_reason or "no_disponible",
        )
        return

    primer_candidato = candidates[0]
    finish_reason = _nombre_seguro(
        getattr(primer_candidato, "finish_reason", None)
    )
    contenido = getattr(primer_candidato, "content", None)
    partes = getattr(contenido, "parts", None) or []
    partes_con_texto = sum(
        1 for parte in partes if getattr(parte, "text", None)
    )

    logger.warning(
        "Candidato de Gemini sin texto usable; candidatos=%d "
        "finish_reason=%s partes_con_texto=%d prompt_feedback_disponible=%s "
        "block_reason=%s",
        len(candidates),
        finish_reason or "no_disponible",
        partes_con_texto,
        prompt_feedback is not None,
        block_reason or "no_disponible",
    )


"...."
def analizar_noticia(titulo, autor="", fecha="", contenido=""):
    """
    Analiza la credibilidad de una noticia usando Gemini AI.

    Args:
        titulo (str): Título de la noticia
        autor (str): Autor del artículo (opcional)
        fecha (str): Fecha de publicación (opcional)
        contenido (str): Contenido completo o resumen de la noticia

    Returns:
        str: Análisis formateado con credibilidad y explicación
    """
    if client is None:
        logger.error("Intento de análisis sin modelo Gemini configurado")
        return ERROR_SIN_API_KEY

    prompt = PROMPT_ANALISIS_NOTICIA.format(
        titulo=titulo,
        autor=autor,
        fecha=fecha,
        contenido=contenido,
    )

    try:
        response = client.models.generate_content(
            model=MODELO_GEMINI,
            contents=prompt,
        )

        if hasattr(response, "text") and response.text:

            logger.info("Análisis de Gemini recibido con texto usable")
            return response.text

        candidates = getattr(response, "candidates", None)
        if candidates:
            parts = getattr(candidates[0].content, "parts", [])
            text_parts = []
            for part in parts:
                if hasattr(part, "text") and part.text:
                    text_parts.append(part.text)
            if text_parts:
                logger.info(
                    "Análisis de Gemini recuperado desde candidates.parts; "
                    "partes_con_texto=%d",
                    len(text_parts),
                )
                return "".join(text_parts)

        _registrar_diagnostico_respuesta(response)
        logger.warning("Respuesta de Gemini sin contenido usable")
        return ERROR_SIN_RESPUESTA_VALIDA

    except Exception as e:
        codigo_status = _obtener_codigo_status(e)
        clasificacion = _clasificar_error(codigo_status)
        logger.error(
            "Error de API de Gemini; tipo=%s status_code=%s "
            "clasificacion=%s",
            type(e).__name__,
            codigo_status or "no_disponible",
            clasificacion,
        )
        return ERROR_ANALIZAR_NOTICIA