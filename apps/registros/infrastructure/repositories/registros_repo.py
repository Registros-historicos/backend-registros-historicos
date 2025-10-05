from apps.registros.domain.entities import Registro
from apps.registros.domain.ports import RegistroRepository
from psycopg2.extensions import AsIs
from django.db import connection


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

        return self._mapear_row_a_registro(row)

    def habilitar(self, id_registro: int) -> None:
        with connection.cursor() as cursor:
            estatus_habilitado = 1
            cursor.execute(
                "SELECT f_habilita_registro(%s, %s)",
                [id_registro, estatus_habilitado]
            )

    def deshabilitar(self, id_registro: int):
        with connection.cursor() as cursor:
            estatus_deshabilitado = 2
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
