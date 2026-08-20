"""
Vistas de la aplicación FakeBuster.

Maneja las solicitudes HTTP para análisis de noticias,
tanto desde URLs como desde entrada manual de usuarios.
"""

import logging
from django.shortcuts import render
from . import article_extractor
from .gemini_service import analizar_noticia
from .constants import (
    ERROR_URL_VACIA,
    ERROR_SITIO_BLOQUEADO,
    ERROR_ANALIZAR_URL,
)
from .utils import validar_url, normalizar_entrada, validar_campos_obligatorios

logger = logging.getLogger(__name__)


def mostrar_valor(request):
    """
    Procesa el análisis de noticias desde URL o formulario manual.

    GET: Muestra el formulario inicial
    POST: Procesa el análisis y devuelve resultados

    Args:
        request: HttpRequest del usuario

    Returns:
        HttpResponse: Template con resultados o formulario con errores
    """
    if request.method == 'POST':
        return procesar_analisis(request)

    return render(request, 'index.html')


def procesar_analisis(request):
    """
    Procesa la solicitud POST de análisis de noticia.

    Determina si es análisis desde URL o manual, valida datos,
    y llama al servicio de Gemini para análisis.

    Args:
        request: HttpRequest del usuario

    Returns:
        HttpResponse: Página de resultados o formulario con errores
    """
    form_id = request.POST.get('form_id')
    titulo = ""
    autor = ""
    fecha = ""
    contenido = ""

    if form_id == 'formularioURL':
        resultado = procesar_analisis_url(request)
        if isinstance(resultado, tuple):
            autor, titulo, fecha, contenido = resultado
        else:
            # Es un error (respuesta HTTP)
            return resultado
    else:
        resultado = procesar_analisis_manual(request)
        if isinstance(resultado, dict):
            # Es un error (diccionario con contexto)
            return render(request, 'index.html', resultado)

        contenido, titulo, autor, fecha = resultado

    # Realizar análisis con Gemini
    logger.info(f"Analizando noticia: {titulo[:50] if titulo else 'Sin título'}...")
    resultado_analisis = analizar_noticia(
        titulo=titulo,
        autor=autor,
        fecha=fecha,
        contenido=contenido
    )

    return render(request, 'respuesta.html', {
        'resultado': resultado_analisis
    })


def procesar_analisis_url(request):
    """
    Procesa el análisis desde una URL de artículo.

    Args:
        request: HttpRequest con parámetro 'url'

    Returns:
        tuple: (autor, titulo, fecha, contenido) si es exitoso
        HttpResponse: Página de error si falla
    """
    url = normalizar_entrada(request.POST.get('url', ''))

    if not url or not validar_url(url):
        logger.warning("URL inválida proporcionada")
        return render(request, 'index.html', {'error': ERROR_URL_VACIA})

    logger.info("Extrayendo artículo desde URL proporcionada")
    resultado_url = article_extractor.obtener_datos_articulo(url)

    if resultado_url == "403_FORBIDDEN":
        logger.warning("Sitio bloqueó acceso automático")
        return render(request, 'index.html', {'error': ERROR_SITIO_BLOQUEADO})

    if resultado_url == (None, None, None, None):
        logger.error("No se pudo analizar la URL proporcionada")
        return render(request, 'index.html', {'error': ERROR_ANALIZAR_URL})

    return resultado_url


def procesar_analisis_manual(request):
    """
    Procesa el análisis desde entrada manual del usuario.

    Args:
        request: HttpRequest con parámetros del formulario manual

    Returns:
        tuple: (contenido, titulo, autor, fecha) si es válido
        dict: Contexto con error si falta información requerida
    """
    contenido = normalizar_entrada(request.POST.get('contenido', ''))
    titulo = normalizar_entrada(request.POST.get('titulo', ''))
    autor = normalizar_entrada(request.POST.get('autor', ''))
    fecha = normalizar_entrada(request.POST.get('fecha', ''))

    # Validar campos obligatorios
    es_valido, mensaje_error = validar_campos_obligatorios(contenido, titulo)
    if not es_valido:
        logger.warning("Formulario manual incompleto")
        return {
            'error': mensaje_error,
            'contenido': contenido,
            'titulo': titulo,
            'autor': autor,
            'fecha': fecha,
        }

    logger.info(f"Análisis manual solicitado para: {titulo[:50]}...")
    return contenido, titulo, autor, fecha