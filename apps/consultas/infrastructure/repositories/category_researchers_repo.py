from django.db import connection

class RegistroRepositorio:
    """
    Capa de acceso a datos que interactúa con la BD de registros.
    """
    def obtener_conteo_por_tipo_investigador(self) -> list[dict]:
        """
        Llama a la función de Postgres f_cuenta_registros_por_tipo_investigador(),
        la une con la tabla parametrizacion para obtener los nombres legibles
        y ordena el resultado por el total de forma descendente.
        """
        # Esta consulta ejecuta la función, une los resultados y los ordena.
        query = """
            SELECT
                p.nombre AS categoria,
                t.total
            FROM
                f_cuenta_registros_por_tipo_investigador() AS t
            INNER JOIN
                parametrizacion AS p ON t.tipo_investigador_param = p.id_param
            ORDER BY
                t.total DESC;
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
    
    def obtener_conteo_global(self) -> list[dict]:
        """
        Conteo global para rol 35 - función f_cuenta_registros_por_tipo_investigador
        """
        query = """
        WITH count AS (
            SELECT tipo_investigador_param, total
            FROM f_cuenta_registros_por_tipo_investigador()
        )
            SELECT
                p.nombre AS categoria,
                COALESCE(t.total, 0) AS total
            FROM parametrizacion AS p
            LEFT JOIN count AS t ON t.tipo_investigador_param = p.id_param
            WHERE p.id_tema = 10
            ORDER BY
                total DESC;
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def obtener_conteo_por_cepat(self, id_cepat: int) -> list[dict]:
        """
        Conteo por CEPAT para rol 37 - función f_cuenta_registros_por_tipo_investigador_cepat
        """
        query = """
        WITH count AS (
            SELECT tipo_investigador_param, total
            FROM f_cuenta_registros_por_tipo_investigador_cepat(%s)
        )
            SELECT
                p.nombre AS categoria,
                COALESCE(t.total, 0) AS total
            FROM parametrizacion AS p
            LEFT JOIN count AS t ON t.tipo_investigador_param = p.id_param
        WHERE p.id_tema = 10
            ORDER BY
                total DESC;
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [id_cepat])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def obtener_conteo_por_institucion(self, id_institucion: int) -> list[dict]:
        """
        Conteo por institución para rol 36 - función f_cuenta_registros_por_tipo_investigador_institucion
        """
        query = """
                WITH count AS (SELECT tipo_investigador_param, total
                               FROM f_cuenta_registros_por_tipo_investigador_institucion(%s))
                SELECT p.nombre             AS categoria,
                       COALESCE(t.total, 0) AS total
                FROM parametrizacion AS p
                         LEFT JOIN count AS t ON t.tipo_investigador_param = p.id_param
                WHERE p.id_tema = 10
                ORDER BY total DESC; \
                """
        with connection.cursor() as cursor:
            cursor.execute(query, [id_institucion])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]