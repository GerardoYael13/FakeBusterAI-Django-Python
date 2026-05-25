import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel(
        "gemini-3.1-flash-lite"
    )

else:
    model = None


def analizar_noticia(titulo, autor="", fecha="", contenido=""):

    if model is None:
        return "No se configuró GOOGLE_API_KEY."

    prompt = f"""
    Eres un analista profesional de noticias y desinformación.

    Fecha actual: 2026.

    Analiza la noticia usando:
    - coherencia del contenido,
    - contexto histórico,
    - eventos conocidos,
    - señales típicas de desinformación,
    - y lógica periodística.

    IMPORTANTE:

    - NO determines automáticamente que algo es falso.
    - NO marques una noticia como dudosa solo porque sea reciente.
    - Considera acontecimientos ampliamente conocidos hasta 2026.
    - Si no existe suficiente información, indícalo moderadamente.
    - Evita respuestas exageradamente conservadoras.
    - No inventes información.

    Datos de la noticia:

    Título:
    {titulo}

    Autor:
    {autor}

    Fecha:
    {fecha}

    Contenido o resumen:
    {contenido}

    Responde EXACTAMENTE usando este formato:

    Credibilidad: Alta / Media / Baja

    Explicación:
    Explica brevemente el análisis.

    Señales sospechosas:
    Menciona posibles señales sospechosas o escribe "No se detectaron señales importantes".

    Conclusión:
    Da una conclusión final clara y profesional.
    """

    try:

        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text

        return "No hubo respuesta válida."

    except Exception as e:
        return f"Error al analizar: {str(e)}"