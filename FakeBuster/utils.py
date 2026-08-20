"""
Utilidades y funciones helper para FakeBuster.

Incluye validadores, procesadores de datos y otras funciones reutilizables
que se usan en múltiples partes de la aplicación.
"""

import re
import logging

logger = logging.getLogger(__name__)


def validar_url(url):
    """
    Valida si una cadena es una URL válida.
    
    Args:
        url (str): La URL a validar
        
    Returns:
        bool: True si la URL es válida, False en caso contrario
    """
    if not url or not isinstance(url, str):
        return False
    
    patron_url = r'^https?://[^\s/$.?#].[^\s]*$'
    es_valida = re.match(patron_url, url, re.IGNORECASE)
    return bool(es_valida)


def normalizar_entrada(texto):
    """
    Normaliza entradas de texto: elimina espacios en blanco
    y caracteres de control innecesarios.
    
    Args:
        texto (str): El texto a normalizar
        
    Returns:
        str: El texto normalizado
    """
    if not isinstance(texto, str):
        return ""
    return texto.strip()


def validar_campos_obligatorios(contenido, titulo):
    """
    Valida que los campos obligatorios del formulario manual no estén vacíos.
    
    Args:
        contenido (str): Contenido o resumen de la noticia
        titulo (str): Título de la noticia
        
    Returns:
        tuple: (es_valido: bool, mensaje_error: str)
    """
    contenido_norm = normalizar_entrada(contenido)
    titulo_norm = normalizar_entrada(titulo)
    
    if not contenido_norm or not titulo_norm:
        from .constants import ERROR_CONTENIDO_FALTANTE
        return False, ERROR_CONTENIDO_FALTANTE
    
    return True, None


def formatear_fecha(fecha_obj):
    """
    Formatea un objeto datetime a string ISO (YYYY-MM-DD).
    
    Args:
        fecha_obj: Objeto datetime o None
        
    Returns:
        str: Fecha formateada o "Fecha desconocida"
    """
    from .constants import FECHA_DESCONOCIDA
    
    if not fecha_obj:
        return FECHA_DESCONOCIDA
    
    try:
        return fecha_obj.strftime("%Y-%m-%d")
    except (AttributeError, ValueError) as e:
        logger.warning(f"No se pudo formatear la fecha: {e}")
        return FECHA_DESCONOCIDA
