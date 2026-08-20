from datetime import datetime
from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase

from .article_extractor import obtener_datos_articulo
from .utils import validar_campos_obligatorios, validar_url


class ArticleExtractorTests(TestCase):
    @patch("FakeBuster.article_extractor.analizar_url")
    def test_obtener_datos_articulo_incluye_texto_del_articulo(self, mock_analizar_url):
        artículo = SimpleNamespace(
            authors=["Ana López"],
            title="Noticia de prueba",
            publish_date=datetime(2024, 1, 15),
            text="Contenido de la noticia para analizar.",
        )
        mock_analizar_url.return_value = artículo

        resultado = obtener_datos_articulo("https://example.com/articulo")

        self.assertEqual(
            resultado,
            ("Ana López", "Noticia de prueba", "2024-01-15", "Contenido de la noticia para analizar."),
        )


class ValidationTests(TestCase):
    def test_validar_url_rechaza_url_invalida(self):
        self.assertFalse(validar_url("texto sin formato"))

    def test_validar_campos_obligatorios_rechaza_manual_incompleto(self):
        es_valido, mensaje_error = validar_campos_obligatorios("", "Título de prueba")

        self.assertFalse(es_valido)
        self.assertIn("contenido", mensaje_error.lower())

    def test_validar_campos_obligatorios_acepta_manual_valido(self):
        es_valido, mensaje_error = validar_campos_obligatorios("Contenido válido", "Título válido")

        self.assertTrue(es_valido)
        self.assertIsNone(mensaje_error)
