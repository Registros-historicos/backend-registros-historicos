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