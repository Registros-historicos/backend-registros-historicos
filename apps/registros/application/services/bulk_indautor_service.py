import pandas as pd
from django.db import transaction, connection
from apps.registros.application.selectors.create_record import create_new_record
from apps.registros.application.selectors.add_investigador_to_registro import add_investigador_to_registro
from apps.registros.infrastructure.repositories.investigadores_repositorio import PostgresInvestigadorRepository


class BulkIndautorService:
    """
    Carga masiva de registros INDAUTOR desde un único Excel:
      - Hoja 'Autores' para investigadores y adscripciones
      - Hojas numéricas (ej. 2025) para registros
    """

    def __init__(self, registros_repo, investigadores_repo=None):
        self.registros_repo = registros_repo
        self.investigadores_repo = investigadores_repo or PostgresInvestigadorRepository()

    def execute(self, file, id_usuario: int, hojas_input: str = None):
        try:
            xls = pd.ExcelFile(file)
        except Exception as e:
            return {"error": f"Error al leer Excel: {e}"}

        hojas_disponibles = xls.sheet_names
        creados_autores, errores_autores = self._procesar_autores(xls)
        creados_registros, actualizados_registros, errores_registros = self._procesar_registros(xls, id_usuario, hojas_input)

        return {
            "mensaje": "Carga masiva completada",
            "autores_creados": creados_autores,
            "errores_autores": len(errores_autores),
            "registros_creados": creados_registros,
            "registros_actualizados": actualizados_registros,
            "errores_registros": len(errores_registros),
            "errores_detalle": {
                "autores": errores_autores,
                "registros": errores_registros
            }
        }

    # === 1️⃣ Carga de autores ===
    def _procesar_autores(self, xls):
        if "AUTORES" not in xls.sheet_names:
            print("⚠️ No se encontró la hoja 'AUTORES', se omite esta parte.")
            return 0, []

        df = pd.read_excel(xls, sheet_name="AUTORES").dropna(how="all")
        creados, errores = 0, []

        for index, row in df.iterrows():
            try:
                curp = str(row.get("CURP (18)", "")).strip()
                if not curp:
                    continue

                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.callproc("f_carga_masiva_investigador_adscripcion", [
                            curp,
                            str(row.get("Nombres (19)", "")).strip() or "SIN NOMBRE",
                            str(row.get("Apellido Paterno (20)", "")).strip() or "",
                            str(row.get("Apellido Materno (21)", "")).strip() or "",
                            int(row.get("Sexo (22)", 1)),
                            int(row.get("Tipo de investigador (23)", 1)),
                            int(row.get("Departamento (27)", 1)),
                            int(row.get("Programa Educativo (25)", 1)),
                            int(row.get("Cuerpo Academico (26)", 1)),
                            pd.to_datetime(row.get("Fecha de Afiliación (28)"), errors="coerce").date() if pd.notna(row.get("Fecha de Afiliación (28)")) else None,
                            pd.to_datetime(row.get("Fecha de Fin (29)"), errors="coerce").date() if pd.notna(row.get("Fecha de Fin (29)")) else None,
                            int(row.get("Institución (24)", 1)),
                        ])
                        result = cursor.fetchall()
                        if result:
                            creados += 1
                            print(f"✅ Autor {curp} procesado correctamente.")
            except Exception as e:
                errores.append({
                    "fila": int(index) + 2,
                    "curp": curp,
                    "error": str(e)
                })
                print(f"❌ Error en autor {curp}: {e}")

        print(f"📗 Autores procesados: {creados} | Errores: {len(errores)}")
        return creados, errores

    # === 2️⃣ Carga de registros INDAUTOR ===
    def _procesar_registros(self, xls, id_usuario, hojas_input):
        hojas_disponibles = [h for h in xls.sheet_names if h.isdigit()]
        hojas_a_cargar = self._parse_hojas(hojas_input, hojas_disponibles)
        creados, actualizados, errores = 0, 0, []

        for hoja in hojas_a_cargar:
            print(f"📘 Procesando hoja de registros: {hoja}")
            preview = pd.read_excel(xls, sheet_name=hoja, nrows=6, header=None)
            header_row = next((i for i, row in preview.iterrows() if any(str(c).strip().startswith("N. Expediente") for c in row)), 4)
            df = pd.read_excel(xls, sheet_name=hoja, header=header_row).dropna(how="all")

            for index, row in df.iterrows():
                expediente = str(row.get("N. Expediente(1)", "")).strip()
                if not expediente:
                    continue

                try:
                    with transaction.atomic():
                        registro_data = {
                            "no_expediente": expediente,
                            "titulo": str(row.get("Título (2)", "")).strip() or None,
                            "descripcion": str(row.get("Descripción (3)", "")).strip() or None,
                            "fec_solicitud": row.get("Fecha de Solicitud (4)"),
                            "no_titulo": str(row.get("N. de Certificado (5)", "")).strip() or None,
                            "estatus_param": self._to_int(row.get("Estatus (6)")),
                            "rama_param": self._to_int(row.get("Rama (7)")),
                            "medio_ingreso_param": self._to_int(row.get("Medio de Ingreso (8)")),
                            "tecnologico_origen": str(row.get("Tecnologico de Origen (9)", "")).strip(),
                            "anio_renovacion": self._to_int(row.get("Año renovación (10)")),
                            "id_subsector": self._to_int(row.get("Subsector (13)")),
                            "fec_expedicion": row.get("Fecha de Expedición (15)"),
                            "archivo": str(row.get("Archivo (16)", "")).strip(),
                            "observaciones": str(row.get("Observaciones (17)", "")).strip(),
                            "tipo_registro_param": 45,
                            "tipo_ingreso_param": 38,  
                            "id_usuario": id_usuario,
                        }

                        registro_existente = self.registros_repo.get_by_expediente(expediente)
                        if registro_existente:
                            actualizados += 1
                            continue

                        create_new_record(registro_data)
                        creados += 1

                        curps_raw = str(row.get("Autores (14)", "")).strip()
                        if not curps_raw:
                            continue
                        curps = [c.strip() for c in curps_raw.split(",") if c.strip()]

                        for curp in curps:
                            investigador_existente = self.investigadores_repo.get_by_curp(curp)
                            if investigador_existente:
                                add_investigador_to_registro(curp, investigador_existente, expediente)
                            else:
                                print(f"⚠️ Investigador {curp} no encontrado (verifica hoja 'Autores').")

                except Exception as e:
                    errores.append({
                        "hoja": hoja,
                        "fila": int(index) + int(header_row) + 2,
                        "expediente": expediente,
                        "error": str(e)
                    })
                    print(f"❌ Error en registro {expediente}: {e}")

        print(f"📘 Registros creados: {creados} | Actualizados: {actualizados} | Errores: {len(errores)}")
        return creados, actualizados, errores

    # === Utilidades ===
    def _parse_hojas(self, hojas_input, hojas_disponibles):
        if not hojas_input:
            return hojas_disponibles
        hojas_input = hojas_input.replace(" ", "")
        if "-" in hojas_input:
            start, end = hojas_input.split("-")
            try:
                rango = [str(y) for y in range(int(start), int(end) + 1)]
                return [h for h in hojas_disponibles if h in rango]
            except ValueError:
                return []
        return [h for h in hojas_input.split(",") if h in hojas_disponibles]

    def _to_int(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
