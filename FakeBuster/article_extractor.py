"""
Extractor de artículos desde URLs.

Utiliza la librería newspaper para descargar y parsear artículos web,
extrayendo título, autor y fecha de publicación.
"""

import logging
from newspaper import Article, ArticleException
from .constants import (
    AUTOR_DESCONOCIDO,
    TITULO_VACIO,
    FECHA_DESCONOCIDA,
    LENGUAJE_ARTICULO,
)
from .utils import formatear_fecha

logger = logging.getLogger(__name__)

# Cache simple de artículos analizados para evitar re-descargas
articulos_cache = {}


def obtener_datos_articulo(url):
    """
    Extrae título, autor, fecha y contenido de un artículo desde su URL.

    Implementa cache simple para evitar re-descargar la misma URL.

    Args:
        url (str): URL del artículo a analizar

    Returns:
        tuple: (autor, titulo, fecha, contenido) si es exitoso
        str: "403_FORBIDDEN" si el sitio bloquea acceso automático
        tuple: (None, None, None, None) si no se pudo procesar la URL
    """
    try:
        # Verificar cache
        if url in articulos_cache:
            article = articulos_cache[url]
        else:
            article = analizar_url(url)
            if article == "403_FORBIDDEN":
                return "403_FORBIDDEN"
            articulos_cache[url] = article

        if not article:
            return None, None, None, None

        # Extraer datos del artículo
        autor = article.authors[0] if article.authors else AUTOR_DESCONOCIDO
        titulo = article.title if article.title else TITULO_VACIO
        fecha = formatear_fecha(article.publish_date)
        contenido = (article.text or article.summary or "").strip()

        return autor, titulo, fecha, contenido

    except Exception as e:
        logger.error(f"Error extrayendo datos del artículo: {e}", exc_info=True)
        return None, None, None, None


def analizar_url(url):
    """
    Descarga y parsea un artículo desde una URL.

    Args:
        url (str): URL del artículo

    Returns:
        Article: Objeto del artículo parseado
        str: "403_FORBIDDEN" si el servidor rechaza la solicitud
        None: Si ocurre otro error
    """
    try:
        article = Article(url, language=LENGUAJE_ARTICULO)
        article.download()
        article.parse()
        return article

    except ArticleException as e:
        error_texto = str(e)
        logger.warning(f"Error ArticleException al analizar artículo: {error_texto}")

        if "403" in error_texto:
            return "403_FORBIDDEN"

        return None