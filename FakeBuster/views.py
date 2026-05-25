from django.shortcuts import render
from . import article_extractor
from .gemini_service import analizar_noticia


def mostrar_valor(request):

    if request.method == 'POST':

        form_id = request.POST.get('form_id')

        contenido = ""

        # ====================================
        # FORMULARIO URL
        # ====================================

        if form_id == 'formularioURL':

            url = request.POST.get('url', '').strip()

            if not url:

                return render(request, 'index.html', {
                    'error': 'Introduce una URL válida.'
                })

            resultado_url = article_extractor.obtener_datos_articulo(url)

            if resultado_url == "403_FORBIDDEN":

                return render(request, 'index.html', {
                    'error': (
                        'Ese sitio bloquea el análisis automático. '
                        'Puedes pegar manualmente el texto o resumen.'
                    )
                })

            if resultado_url == (None, None, None):

                return render(request, 'index.html', {
                    'error': (
                        'No se pudo analizar la URL. '
                        'Intenta usar el análisis manual.'
                    )
                })

            autor, titulo, fecha = resultado_url

        # ====================================
        # FORMULARIO MANUAL
        # ====================================

        else:

            contenido = request.POST.get('contenido', '').strip()

            titulo = request.POST.get('titulo', '').strip()

            autor = request.POST.get('autor', '').strip()

            fecha = request.POST.get('fecha', '').strip()

            if not contenido or not titulo:

                return render(request, 'index.html', {
                    'error': (
                        'Completa al menos el contenido/resumen '
                        'y el título.'
                    ),
                    'contenido': contenido,
                    'titulo': titulo,
                    'autor': autor,
                    'fecha': fecha,
                })

        resultado = analizar_noticia(
            titulo=titulo,
            autor=autor,
            fecha=fecha,
            contenido=contenido
        )

        return render(request, 'respuesta.html', {
            'resultado': resultado
        })

    return render(request, 'index.html')