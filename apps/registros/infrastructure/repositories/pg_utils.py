import psycopg2
import psycopg2.extras
from django.conf import settings


def get_connection():
    """
    Crea una conexión a la base de datos PostgreSQL usando la configuración de Django.
    """
    return psycopg2.connect(
        dbname=settings.DATABASES["default"]["NAME"],
        user=settings.DATABASES["default"]["USER"],
        password=settings.DATABASES["default"]["PASSWORD"],
        host=settings.DATABASES["default"]["HOST"],
        port=settings.DATABASES["default"]["PORT"],
        cursor_factory=psycopg2.extras.RealDictCursor,  # devuelve resultados como dict
    )


def run_query(query: str, params=None, fetchone=False, fetchall=False):
    """
    Ejecuta una consulta SQL genérica.

    Args:
        query (str): Consulta SQL.
        params (tuple|list|dict): Parámetros para la consulta.
        fetchone (bool): Si se desea retornar solo una fila.
        fetchall (bool): Si se desean retornar todas las filas.

    Returns:
        dict | list[dict] | None: Resultados de la consulta o None si no hay retorno.
    """
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)

        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        else:
            result = None

        conn.commit()
        return result

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Error en run_query(): {e}\nSQL: {query}\nParams: {params}")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
