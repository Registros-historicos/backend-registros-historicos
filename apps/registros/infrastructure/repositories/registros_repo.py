from typing import Optional
from apps.registros.domain.entities import Registro
from apps.registros.domain.ports import RegistroRepository
from psycopg2.extensions import AsIs
from django.db import connection, transaction
from apps.registros.infrastructure.repositories.pg_utils import run_query

class PostgresRegistroRepository(RegistroRepository):

    def insertar(self, registro: Registro) -> dict:
        with connection.cursor() as cursor:
            cursor.execute("""
                           INSERT INTO registro (no_expediente, titulo, tipo_ingreso_param, id_usuario,
                                                 rama_param, fec_expedicion, observaciones, archivo,
                                                 estatus_param, medio_ingreso_param, tipo_registro_param,
                                                 fec_solicitud, descripcion, tipo_sector_param)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING
                    id_registro,
                    no_expediente,
                    titulo,
                    tipo_ingreso_param,
                    id_usuario,
                    rama_param,
                    fec_expedicion,
                    observaciones,
                    archivo,
                    estatus_param,
                    medio_ingreso_param,
                    tipo_registro_param,
                    fec_solicitud,
                    descripcion,
                    tipo_sector_param;
                           """, [
                               registro.no_expediente,
                               registro.titulo,
                               registro.tipo_ingreso_param,
                               registro.id_usuario,
                               registro.rama_param,
                               registro.fec_expedicion,
                               registro.observaciones,
                               registro.archivo,
                               registro.estatus_param,
                               registro.medio_ingreso_param,
                               registro.tipo_registro_param,
                               registro.fec_solicitud,
                               registro.descripcion,
                               registro.tipo_sector_param,
                           ])
            inserted_row = cursor.fetchone()
            if inserted_row:
                column_names = [desc[0] for desc in cursor.description]
                return dict(zip(column_names, inserted_row))

            return None

    def actualizar(self, id_registro: int, registro: Registro) -> Registro:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT f_actualiza_resgistro_por_pk(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, [
                    id_registro,
                registro.no_expediente,
                registro.titulo,
                registro.tipo_ingreso_param,
                registro.id_usuario,
                registro.rama_param,
                registro.fec_expedicion,
                registro.observaciones,
                registro.archivo,
                registro.estatus_param,
                registro.medio_ingreso_param,
                registro.tipo_registro_param,
                registro.fec_solicitud,
                registro.descripcion,
                registro.tipo_sector_param,
                ])

                cursor.execute("SELECT * FROM registro WHERE id_registro = %s", [id_registro])
                row = cursor.fetchone()

                if not row:
                    raise ValueError(f"No se encontró el registro con id {id_registro}")

        return self._mapear_row_a_registro(row)

    def habilitar(self, id_registro: int) -> None:
        with connection.cursor() as cursor:
            estatus_habilitado = 24
            cursor.execute(
                "SELECT f_habilita_registro(%s, %s)",
                [id_registro, estatus_habilitado]
            )

    def deshabilitar(self, id_registro: int):
        with connection.cursor() as cursor:
            estatus_deshabilitado = 25
            cursor.execute(
                "SELECT * FROM f_deshabilita_registro(%s, %s)",
                [id_registro, estatus_deshabilitado]
            )
            resultado = cursor.fetchall()
            return resultado

    def _mapear_row_a_registro(self, row) -> Registro:
        return Registro(
            id_registro=row[0],
            no_expediente=row[1],
            titulo=row[2],
            tipo_ingreso_param=row[3],
            id_usuario=row[4],
            rama_param=row[5],
            fec_expedicion=row[6],
            observaciones=row[7],
            archivo=row[8],
            estatus_param=row[9],
            medio_ingreso_param=row[10],
            tipo_registro_param=row[11],
            fec_solicitud=row[12],
            descripcion=row[13],
            tipo_sector_param=row[14],
        )

    def listar_por_tipo(self, tipo_registro_param: int, limit: int, offset: int, filter: str, order: str) -> list[dict]:
        """ Lista registros por tipo con paginación """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM f_busca_registros_por_tipo(%s, %s, %s, %s, %s)
            """, [tipo_registro_param, limit, offset, filter, order])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    def contar_por_tipo(self, tipo_registro_param: int) -> int:
        """ Cuenta total de registros por tipo """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT f_cuenta_registros_por_tipo(%s)
            """, [tipo_registro_param])
            rows = cursor.fetchall()
            total = sum(int(row[-1].strip('()').split(',')[-1]) for row in rows)

            return total

            
    def buscar_por_texto(self, tipo_registro_param: int, texto: str, limit: int, offset: int) -> list[dict]:
        """ Busca registros por texto con paginación """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM f_busca_registros_por_texto(%s, %s, %s, %s)
            """, [tipo_registro_param, texto, limit, offset])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def contar_por_texto(self, tipo_registro_param: int, texto: str) -> int:
        """ Cuenta registros que coinciden con el texto """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT f_contar_registros_por_texto(%s, %s)
            """, [tipo_registro_param, texto])
            return cursor.fetchone()[0] or 0
        
    def obtener_por_id(self, id_registro: int) -> Optional[dict]:
        """ Obtiene un registro por su ID """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM f_busca_registro_por_pk(%s)
            """, [id_registro])
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def obtener_por_expediente(self, no_expediente: str) -> Optional[dict]:
        """ Obtiene un registro por número de expediente """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM f_busca_registro_por_numero_de_expediente(%s)
            """, [no_expediente])
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None



    def upsert(self, reg):
        """
        Inserta o actualiza un registro en la tabla 'registro' con base en 'no_expediente'.
        """
        query = """
        INSERT INTO registro (
            no_expediente, titulo, descripcion, fec_solicitud,
            no_titulo, estatus_param, rama_param, medio_ingreso_param,
            tecnologico_origen, anio_renovacion, id_subsector,
            fec_expedicion, archivo, observaciones,
            tipo_registro_param, tipo_ingreso_param, id_usuario
        ) VALUES (
            %(no_expediente)s, %(titulo)s, %(descripcion)s, %(fec_solicitud)s,
            %(no_titulo)s, %(estatus_param)s, %(rama_param)s, %(medio_ingreso_param)s,
            %(tecnologico_origen)s, %(anio_renovacion)s, %(id_subsector)s,
            %(fec_expedicion)s, %(archivo)s, %(observaciones)s,
            %(tipo_registro_param)s, %(tipo_ingreso_param)s, %(id_usuario)s
        )
        ON CONFLICT (no_expediente)
        DO UPDATE SET
            titulo = EXCLUDED.titulo,
            descripcion = EXCLUDED.descripcion,
            fec_solicitud = EXCLUDED.fec_solicitud,
            no_titulo = EXCLUDED.no_titulo,
            estatus_param = EXCLUDED.estatus_param,
            rama_param = EXCLUDED.rama_param,
            medio_ingreso_param = EXCLUDED.medio_ingreso_param,
            tecnologico_origen = EXCLUDED.tecnologico_origen,
            anio_renovacion = EXCLUDED.anio_renovacion,
            id_subsector = EXCLUDED.id_subsector,
            fec_expedicion = EXCLUDED.fec_expedicion,
            archivo = EXCLUDED.archivo,
            observaciones = EXCLUDED.observaciones,
            tipo_registro_param = EXCLUDED.tipo_registro_param,
            tipo_ingreso_param = EXCLUDED.tipo_ingreso_param,
            id_usuario = EXCLUDED.id_usuario
        RETURNING *, (xmax = 0) AS created;
        """

        params = {
            "no_expediente": reg.no_expediente,
            "titulo": reg.titulo,
            "descripcion": reg.descripcion,
            "fec_solicitud": reg.fec_solicitud,
            "no_titulo": reg.no_titulo,
            "estatus_param": reg.estatus_param,
            "rama_param": reg.rama_param,
            "medio_ingreso_param": reg.medio_ingreso_param,
            "tecnologico_origen": reg.tecnologico_origen,
            "anio_renovacion": reg.anio_renovacion,
            "id_subsector": reg.id_subsector,
            "fec_expedicion": reg.fec_expedicion,
            "archivo": reg.archivo,
            "observaciones": reg.observaciones,
            "tipo_registro_param": reg.tipo_registro_param,
            "tipo_ingreso_param": reg.tipo_ingreso_param,
            "id_usuario": reg.id_usuario,
        }

        return run_query(query, params, fetchone=True)

    def get_by_expediente(self, no_expediente: str):
        """
        Retorna un registro por número de expediente.
        """
        query = "SELECT * FROM registro WHERE no_expediente = %s;"
        return run_query(query, [no_expediente], fetchone=True)

    def vincular_investigador(self, id_registro: int, id_investigador: int):
        """
        Inserta la relación entre registro e investigador (por id_investigador).
        Evita duplicados con ON CONFLICT.
        """
        query = """
            INSERT INTO registro_investigador (id_registro, id_investigador)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """
        run_query(query, [id_registro, id_investigador])
