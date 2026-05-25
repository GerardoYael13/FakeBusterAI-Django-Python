# FakeBuster AI

## Descripción

FakeBuster AI es una aplicación web desarrollada con Django y Gemini AI enfocada en el análisis automatizado de credibilidad de noticias y contenido informativo.

El sistema permite analizar noticias mediante:
- URLs de artículos,
- contenido escrito manualmente,
- resúmenes,
- o texto completo proporcionado por el usuario.

A partir de esta información, el sistema genera una evaluación de credibilidad utilizando inteligencia artificial y presenta el resultado de manera visual e intuitiva.

---

## Contexto del proyecto

Este proyecto comenzó como una base académica desarrollada en equipo y posteriormente fue mejorado y adaptado individualmente mediante:
- corrección de errores,
- rediseño visual,
- mejoras en la experiencia de usuario,
- optimización de prompts para IA,
- manejo de errores de extracción,
- y refinamiento general del sistema.

El objetivo principal del proyecto es experimentar con integración de inteligencia artificial aplicada al análisis de contenido digital y detección de posibles señales de desinformación.

---

## Equipo original del proyecto

Proyecto desarrollado originalmente en colaboración con:

- @danielisaisal
- @memotas98
- @OzielLM
- @Rogelio-CC
- @GerardoYael13

---

## Mejoras y mantenimiento posterior

Las mejoras actuales implementadas en este repositorio incluyen:

- Integración mejorada con Gemini AI.
- Corrección de errores de entorno virtual y dependencias.
- Compatibilidad con versiones modernas de Python y librerías.
- Manejo de errores para URLs bloqueadas (403).
- Sistema de análisis manual alternativo.
- Rediseño visual de formularios y resultados.
- Clasificación visual dinámica de credibilidad.
- Mejoras en prompts para respuestas más coherentes y contextualizadas.
- Corrección de rutas y navegación en Django.
- Optimización de experiencia de usuario.

---

## ¿Qué hace este proyecto?

- Extrae información de noticias mediante URLs usando `newspaper3k`.
- Permite análisis manual mediante texto o resúmenes.
- Utiliza Gemini AI para generar un análisis contextual.
- Clasifica visualmente la credibilidad del contenido.
- Detecta posibles inconsistencias o señales de desinformación.
- Presenta resultados de forma clara para el usuario.

---

## Características principales

### 1. Análisis mediante URL

El usuario puede pegar una URL y el sistema intenta extraer:
- título,
- autor,
- fecha,
- y contenido de la noticia.

Posteriormente la información se envía a Gemini AI para su análisis.

---

### 2. Análisis manual

Cuando una página bloquea el acceso automático o el usuario desea mayor control, es posible ingresar:
- texto completo,
- resumen,
- título,
- autor,
- y fecha manualmente.

---

### 3. Clasificación visual inteligente

La respuesta generada por la IA se interpreta automáticamente para mostrar estados visuales como:

- ✅ Probablemente confiable
- ⚠ Requiere verificación
- ❌ Posiblemente engañosa

Esto mejora la interpretación del resultado para el usuario final.

---

## Cómo funciona internamente

- `FakeBuster/views.py` gestiona el formulario y decide si usar la URL o el contenido manual.
- `FakeBuster/article_extractor.py` obtiene datos desde la URL con `newspaper3k`.
- `FakeBuster/gemini_service.py` construye el prompt y llama al modelo Gemini.
- `FakeBuster/templates/index.html` y `FakeBuster/templates/respuesta.html` presentan la UI.

---

## Dependencias

El proyecto utiliza:

- `Django==4.2.5`
- `newspaper3k`
- `google-genai`
- `python-dotenv`
- `lxml_html_clean`

---

## Instalación

1. Clonar el repositorio:

```bash
git clone <repositorio>
cd FakeBusterAI-Django-Python/
```

2. Crear y activar un entorno virtual:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Crear y configurar el archivo `.env`:

```bash
copy .env.example .env
```

Editar `.env` con:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=True`
- `DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost`
- `GOOGLE_API_KEY=<tu_api_key>

5. Ejecutar migraciones:

```bash
python manage.py migrate
```

6. Levantar el servidor:

```bash
python manage.py runserver
```

7. Abrir la aplicación en el navegador:

```text
http://127.0.0.1:8000/
```

---

## Variables de entorno necesarias

- `GOOGLE_API_KEY`: clave de Google Gemini.
- `DJANGO_SECRET_KEY`: clave secreta de Django.
- `DJANGO_DEBUG`: controla el modo debug.
- `DJANGO_ALLOWED_HOSTS`: hosts permitidos.

---

## Limitaciones importantes

- No realiza verificación web en tiempo real.
- No consulta fuentes oficiales automáticamente.
- No es un servicio de fact-checking profesional.
- El análisis depende del contenido provisto y puede no ser definitivo.

Una noticia real puede aparecer como dudosa, y una noticia falsa muy bien redactada puede parecer creíble.

---

## Consideraciones sobre la IA

Gemini AI no realiza navegación web automática en tiempo real dentro de este proyecto.

El análisis se basa únicamente en:

- la información extraída desde la URL,
- o el contenido proporcionado manualmente por el usuario.

Por esta razón:

- eventos muy recientes,
- rumores virales,
- información de redes sociales,
- o noticias sin suficiente contexto textual

pueden generar resultados ambiguos o requerir verificación adicional.

Este sistema debe considerarse una herramienta experimental de apoyo y no una fuente definitiva de verificación periodística.

---

## Estructura del proyecto

```
FakeBuster-Django-Python-main/
├── FakeBuster/
│   ├── views.py
│   ├── urls.py
│   ├── gemini_service.py
│   ├── article_extractor.py
│   ├── templates/
│   │   ├── index.html
│   │   └── respuesta.html
│   └── static/
│       ├── styles.css
│       └── stylesResultados.css
├── FakeBusterWeb/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── db.sqlite3
```

---

## Mejoras implementadas

- Mejor manejo de errores al analizar URLs bloqueadas.
- Mensajes de usuario más claros.
- Ajustes en la generación de respuestas para mejorar claridad y consistencia del análisis.
- UI más limpia con indicadores de credibilidad.

---

## Posibles mejoras futuras

- Integrar almacenamiento de resultados.
- Añadir historial de análisis.
- Implementar autenticación de usuarios.
- Agregar dashboard administrativo.
- Buscar fuentes externas en tiempo real.
- Usar APIs de verificación de hechos.

---

## Nota final

FakeBuster AI es un proyecto experimental enfocado en la integración de inteligencia artificial para el análisis automatizado de contenido informativo.

