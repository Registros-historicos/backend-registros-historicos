from typing import Optional
from apps.registros.domain.entities import Registro
from apps.registros.domain.ports import RegistroRepository
from psycopg2.extensions import AsIs
from django.db import connection, transaction
from apps.registros.infrastructure.repositories.pg_utils import run_query
from datetime import datetime, date

from apps.users.application.selectors.resolve_user_context import resolve_user_context

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

    def limpiar_campo(self, valor):
        return valor if valor not in ("", None) else None

    def actualizar(self, id_registro: int, registro: Registro) -> Registro:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT public.f_actualiza_resgistro_por_pk(
                        %s,  -- p_id_registro (obligatorio)
                        %s,  -- p_titulo
                        %s,  -- p_tipo_ingreso_param
                        %s,  -- p_id_usuario
                        %s,  -- p_rama_param
                        %s,  -- p_fec_expedicion
                        %s,  -- p_observaciones
                        %s,  -- p_archivo
                        %s,  -- p_estatus_param
                        %s,  -- p_medio_ingreso_param
                        %s,  -- p_tipo_registro_param
                        %s,  -- p_fec_solicitud
                        %s,  -- p_descripcion
                        %s,  -- p_tecnologico_origen
                        %s,  -- p_anio_renovacion
                        %s   -- p_id_subsector
                    )
                    """,
                    [
                        registro.id_registro,
                        self.limpiar_campo(registro.titulo),
                        self.limpiar_campo(registro.tipo_ingreso_param),
                        self.limpiar_campo(registro.id_usuario),
                        self.limpiar_campo(registro.rama_param),
                        self.limpiar_campo(registro.fec_expedicion),
                        self.limpiar_campo(registro.observaciones),
                        self.limpiar_campo(registro.archivo),
                        self.limpiar_campo(registro.estatus_param),
                        self.limpiar_campo(registro.medio_ingreso_param),
                        self.limpiar_campo(registro.tipo_registro_param),
                        self.limpiar_campo(registro.fec_solicitud),
                        self.limpiar_campo(registro.descripcion),
                        self.limpiar_campo(registro.tecnologico_origen),
                        self.limpiar_campo(registro.anio_renovacion),
                        self.limpiar_campo(registro.id_subsector),
                    ]
                )

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

    def _to_date_or_none(self, value):
        if isinstance(value, datetime):
            return value.date()
        return value

    def _mapear_row_a_registro(self, row) -> Registro:
        return Registro(
            id_registro=row[0],
            no_expediente=None,
            titulo=row[2],
            tipo_ingreso_param=row[3],
            rama_param=row[4],
            fec_expedicion=self._to_date_or_none(row[5]),
            observaciones=row[6],
            archivo=row[7],
            estatus_param=row[8],
            medio_ingreso_param=row[9],
            tipo_registro_param=row[10],
            fec_solicitud=self._to_date_or_none(row[11]),
            descripcion=row[12],
            id_usuario=row[13],
            tipo_sector_param=None,
            tecnologico_origen=row[15],
            anio_renovacion=row[16],
            id_subsector=row[17],
        )



    def listar_por_tipo(self,  tipo_registro_param: int,
                        limit: int, offset: int, sort_column: str, sort_order: str, id_usuario: int,) -> list[dict]:
        """
        Lista registros por tipo tomando en cuenta el ROL:
        - Rol 37 (CePaT): filtra por CEPA(T)
        - Rol 36 (Coordinador): filtra por institución asignada
        - Otros roles: función global sin filtros
        """

        # OBTENER CONTEXTO DEL USUARIO
        ctx = resolve_user_context(id_usuario)
        if not ctx:
            raise ValueError("No se pudo resolver el contexto del usuario")

        rol = ctx.get("rol_id")
        id_institucion = ctx.get("id_institucion")
        id_cepat = ctx.get("id_cepat")

        sort_column = sort_column or "fec_solicitud"
        sort_order = sort_order or "DESC"

        with connection.cursor() as cursor:

            if rol == 37 and id_cepat:
                cursor.execute(
                    """
                    SELECT *
                    FROM f_busca_registros_por_tipo_y_cepat(%s, %s, %s, %s, %s, %s)
                    """,
                    [
                        tipo_registro_param,
                        id_cepat,
                        limit,
                        offset,
                        sort_column,
                        sort_order
                    ]
                )

            elif rol == 36 and id_institucion:
                cursor.execute(
                    """
                    SELECT *
                    FROM f_busca_registros_por_tipo_y_institucion(%s, %s, %s, %s, %s, %s)
                    """,
                    [
                        tipo_registro_param,
                        id_institucion,
                        limit,
                        offset,
                        sort_column,
                        sort_order
                    ]
                )

            else:
                cursor.execute(
                    """
                    SELECT *
                    FROM f_busca_registros_por_tipo(%s, %s, %s, %s, %s)
                    """,
                    [
                        tipo_registro_param,
                        limit,
                        offset,
                        sort_column,
                        sort_order
                    ]
                )

            # Convertir resultados a dict
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def contar_por_tipo(self, tipo_registro_param: int, id_usuario: int = None) -> int:
        """
        Cuenta registros por tipo según el rol del usuario:
        - Admin (35): global
        - CePaT (37): filtra por CEPA
        - Coordinador (36): filtra por instituciones asignadas
        """
        # Resolver contexto
        ctx = resolve_user_context(id_usuario) if id_usuario else None
        if not ctx:
            raise ValueError("No se pudo resolver el contexto del usuario")

        rol = ctx.get("rol_id")
        id_cepat = ctx.get("id_cepat")
        instituciones = ctx.get("instituciones")  # lista []
        
        with connection.cursor() as cursor:

            if rol == 35:
                cursor.execute(
                    """SELECT * FROM f_cuenta_registros_por_tipo(%s)""",
                    [tipo_registro_param]
                )
                rows = cursor.fetchall()
                return sum(row[-1] for row in rows)

            if rol == 37 and id_cepat:
                cursor.execute(
                    """SELECT * FROM f_cuenta_registros_por_tipo_cepat(%s, %s)""",
                    [tipo_registro_param, id_cepat]
                )
                rows = cursor.fetchall()
                return sum(row[-1] for row in rows)

            # ➤ COORDINADOR → lista de instituciones asociadas
            if rol == 36 and instituciones:
                cursor.execute(
                    """SELECT * FROM f_cuenta_registros_por_tipo_instituciones(%s, %s)""",
                    [tipo_registro_param, instituciones]
                )
                rows = cursor.fetchall()
                return sum(row[-1] for row in rows)

            # ➤ Cualquier otro rol → global
            cursor.execute(
                """SELECT * FROM f_cuenta_registros_por_tipo(%s)""",
                [tipo_registro_param]
            )
            rows = cursor.fetchall()
            return sum(row[-1] for row in rows)
            
    def buscar_por_texto(self, tipo_registro_param: int, texto: str,
                        limit: int, offset: int, sort_column: str,
                        sort_order: str, id_usuario: int) -> list[dict]:

        # Resolver contexto
        ctx = resolve_user_context(id_usuario)
        if not ctx:
            raise ValueError("No se pudo resolver el contexto del usuario")

        rol = ctx.get("rol_id")
        id_cepat = ctx.get("id_cepat")
        id_institucion = ctx.get("id_institucion")

        with connection.cursor() as cursor:

            # --- 🔵 CePaT ---
            if rol == 37 and id_cepat:
                cursor.execute("""
                    SELECT *
                    FROM f_busca_registros_por_texto_y_cepat(%s, %s, %s, %s, %s, %s, %s)
                """, [
                    tipo_registro_param,
                    texto,
                    id_cepat,
                    limit,
                    offset,
                    sort_column,
                    sort_order
                ])

            # --- 🟢 Coordinador ---
            elif rol == 36 and id_institucion:
                cursor.execute("""
                    SELECT *
                    FROM f_busca_registros_por_texto_y_institucion(%s, %s, %s, %s, %s, %s, %s)
                """, [
                    tipo_registro_param,
                    texto,
                    id_institucion,
                    limit,
                    offset,
                    sort_column,
                    sort_order
                ])

            # --- 🔴 Admin / global ---
            else:
                cursor.execute("""
                    SELECT *
                    FROM f_busca_registros_por_texto(%s, %s, %s, %s, %s, %s)
                """, [
                    tipo_registro_param,
                    texto,
                    limit,
                    offset,
                    sort_column,
                    sort_order
                ])

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]



    def contar_por_texto(self, tipo_registro_param: int, texto: str, id_usuario: int) -> int:
        """Cuenta registros que coinciden con el texto considerando el ROL del usuario."""

        # Resolver contexto del usuario
        ctx = resolve_user_context(id_usuario)
        if not ctx:
            raise ValueError("No se pudo resolver el contexto del usuario")

        rol = ctx.get("rol_id")
        id_cepat = ctx.get("id_cepat")
        id_institucion = ctx.get("id_institucion")

        with connection.cursor() as cursor:

            # --- 🔵 CePaT ---
            if rol == 37 and id_cepat:
                cursor.execute(
                    """
                    SELECT f_contar_registros_por_texto_y_cepat(%s, %s, %s)
                    """,
                    [tipo_registro_param, texto, id_cepat]
                )
                return cursor.fetchone()[0] or 0

            # --- 🟢 Coordinador ---
            elif rol == 36 and id_institucion:
                cursor.execute(
                    """
                    SELECT f_contar_registros_por_texto_y_institucion(%s, %s, %s)
                    """,
                    [tipo_registro_param, texto, id_institucion]
                )
                return cursor.fetchone()[0] or 0

            # --- 🔴 Admin u otros roles (global) ---
            else:
                cursor.execute(
                    """
                    SELECT f_contar_registros_por_texto(%s, %s)
                    """,
                    [tipo_registro_param, texto]
                )
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

    def obtener_investigadores_por_registro(self, id_registro: int):
        query = """
            SELECT DISTINCT ON (i.id_investigador)
                i.id_investigador,
                i.curp,
                i.nombre,
                i.ape_pat,
                i.ape_mat,
                i.sexo_param,
                i.tipo_investigador_param,
                a.id_adscripcion,
                a.id_institucion,
                a.departamento_param,
                a.programa_educativo_param,
                a.cuerpo_academico_param,
                a.fec_ini,
                a.fec_fin
            FROM public.registro_investigador ri
            JOIN public.investigador i
            ON i.id_investigador = ri.id_investigador
            LEFT JOIN public.adscripcion a
            ON a.id_investigador = i.id_investigador
            AND (a.fec_fin IS NULL OR a.fec_fin > NOW())
            WHERE ri.id_registro = %s
            ORDER BY i.id_investigador, a.fec_ini DESC;
        """
        return run_query(query, [id_registro], fetchall=True) or []

