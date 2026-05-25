from newspaper import Article, ArticleException

# Cache simple
articulos_cache = {}

def obtener_datos_articulo(url):

    try:

        if url in articulos_cache:
            article = articulos_cache[url]
        else:
            article = analizar_url(url)

            if article == "403_FORBIDDEN":
                return "403_FORBIDDEN"

            articulos_cache[url] = article

        if not article:
            return None, None, None

        autor = article.authors[0] if article.authors else "Autor desconocido"

        titulo = article.title if article.title else ""

        fecha = (
            article.publish_date.strftime("%Y-%m-%d")
            if article.publish_date
            else "Fecha desconocida"
        )

        return autor, titulo, fecha

    except Exception as e:
        print(f"Error general: {e}")
        return None, None, None


def analizar_url(url):

    try:

        article = Article(url, language='es')

        article.download()
        article.parse()

        return article

    except ArticleException as e:

        error_texto = str(e)

        print(f"Error al analizar URL: {url}. Error: {error_texto}")

        if "403" in error_texto:
            return "403_FORBIDDEN"

        return None