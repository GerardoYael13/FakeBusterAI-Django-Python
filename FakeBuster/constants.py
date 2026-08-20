"""
Constantes y configuraciones de la aplicación FakeBusterAI.

Centraliza todos los textos, prompts y mensajes para facilitar mantenimiento
y traducción futura.
"""

# Mensajes de error - Formulario URL
ERROR_URL_VACIA = "Introduce una URL válida."
ERROR_SITIO_BLOQUEADO = (
    "Ese sitio bloquea el análisis automático. "
    "Puedes pegar manualmente el texto o resumen."
)
ERROR_ANALIZAR_URL = (
    "No se pudo analizar la URL. "
    "Intenta usar el análisis manual."
)

# Mensajes de error - Formulario Manual
ERROR_CONTENIDO_FALTANTE = (
    "Completa al menos el contenido/resumen y el título."
)

# Mensajes de error - Servicio Gemini
ERROR_SIN_API_KEY = "No se configuró GOOGLE_API_KEY."
ERROR_SIN_RESPUESTA_VALIDA = "No hubo respuesta válida."
ERROR_ANALIZAR_NOTICIA = "Error al analizar"

# Valores por defecto
AUTOR_DESCONOCIDO = "Autor desconocido"
FECHA_DESCONOCIDA = "Fecha desconocida"
TITULO_VACIO = ""

# Configuración de modelos
MODELO_GEMINI = "gemini-3.1-flash-lite"
LENGUAJE_ARTICULO = "es"

# Prompt base para análisis de noticias
PROMPT_ANALISIS_NOTICIA = """Eres un analista profesional de noticias y desinformación.

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
Da una conclusión final clara y profesional."""
