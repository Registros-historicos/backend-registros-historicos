import pandas as pd
from django.db import transaction, connection
from apps.registros.application.selectors.create_record import create_new_record
from apps.registros.application.selectors.add_investigador_to_registro import add_investigador_to_registro
from apps.registros.infrastructure.repositories.investigadores_repositorio import PostgresInvestigadorRepository


class BulkImpiService:
    """
    Carga masiva de registros IMPI desde un único Excel:
      - Hoja 'AUTORES' para investigadores y adscripciones
      - Hojas numéricas (ej. 2025) para registros IMPI
    """

    def __init__(self, registros_repo, investigadores_repo=None):
        self.registros_repo = registros_repo
        self.investigadores_repo = investigadores_repo or PostgresInvestigadorRepository()

        # Temas base para buscar id_param cuando vienen como texto
        self.temas = {
            "Sexo": 1,
            "Sector": 2,
            "Rama": 3,
            "Medio de Ingreso": 4,
            "Estatus": 7,
            "TipInvestigador": 10,
            "Departamento": 11,
            "Programa Educativo": 12,
            "Cuerpo Academico": 13,
        }

    # ==========================================================
    # 🚀 EJECUCIÓN PRINCIPAL
    # ==========================================================
    def execute(self, file, id_usuario: int, hojas_input: str = None):
        try:
            xls = pd.ExcelFile(file)
        except Exception as e:
            return {"error": f"Error al leer Excel: {e}"}

        print(f"📄 Archivo recibido: {file}")
        print("📄 Hojas disponibles:", xls.sheet_names)

        # 1️⃣ Procesar autores
        creados_autores, errores_autores = self._procesar_autores(xls)

        # 2️⃣ Procesar registros IMPI
        creados_registros, actualizados_registros, errores_registros = self._procesar_registros(
            xls, id_usuario, hojas_input
        )

        return {
            "mensaje": "Carga masiva completada (IMPI)",
            "autores_creados": creados_autores,
            "errores_autores": len(errores_autores),
            "registros_creados": creados_registros,
            "registros_actualizados": actualizados_registros,
            "errores_registros": len(errores_registros),
            "errores_detalle": {
                "autores": errores_autores,
                "registros": errores_registros,
            },
        }

    # ==========================================================
    # 👩‍🔬 1️⃣ CARGA DE AUTORES
    # ==========================================================
    def _procesar_autores(self, xls):
        if "AUTORES" not in xls.sheet_names:
            print("⚠️ No se encontró la hoja 'AUTORES', se omite esta parte.")
            return 0, []

        print("✅ Se encontró la hoja 'AUTORES', iniciando procesamiento.")
        preview = pd.read_excel(xls, sheet_name="AUTORES", nrows=10, header=None)

        # 🔎 Buscar la fila que contiene 'CURP'
        header_row = next(
            (i for i, row in preview.iterrows()
             if any(str(c).strip().upper().startswith("CURP") for c in row)),
            0
        )

        df = pd.read_excel(xls, sheet_name="AUTORES", header=header_row).dropna(how="all")
        df.columns = [str(c).replace("\xa0", " ").strip() for c in df.columns]

        curp_col = next((c for c in df.columns if "CURP" in c.upper()), None)
        if not curp_col:
            print("❌ No se encontró la columna CURP en la hoja AUTORES.")
            print("📋 Columnas detectadas:", df.columns.tolist())
            return 0, []

        creados, errores = 0, []

        for index, row in df.iterrows():
            curp = str(row.get(curp_col, "")).strip()
            if not curp or curp.lower() == "nan":
                continue

            try:
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.callproc("f_carga_masiva_investigador_adscripcion", [
                            curp,
                            str(row.get("Nombres (20)", "")).strip() or "SIN NOMBRE",
                            str(row.get("Apellido Paterno (21)", "")).strip() or "",
                            str(row.get("Apellido Materno (22)", "")).strip() or "",
                            self._resolve_param_mixto(row.get("Sexo (23)"), self.temas["Sexo"]),
                            self._resolve_param_mixto(row.get("Tipo de investigador (24)"), self.temas["TipInvestigador"]),
                            self._resolve_param_mixto(row.get("Departamento (28)"), self.temas["Departamento"]),
                            self._resolve_param_mixto(row.get("Programa Educativo (26)"), self.temas["Programa Educativo"]),
                            self._resolve_param_mixto(row.get("Cuerpo Academico (27)"), self.temas["Cuerpo Academico"]),
                            pd.to_datetime(row.get("Fecha de Afiliación (29)"), errors="coerce").date()
                                if pd.notna(row.get("Fecha de Afiliación (29)")) else None,
                            pd.to_datetime(row.get("Fecha de Fin (30)"), errors="coerce").date()
                                if pd.notna(row.get("Fecha de Fin (30)")) else None,
                            self._resolve_institucion_id(row.get("Institución (25)")),
                        ])
                        result = cursor.fetchall()
                        if result:
                            creados += 1
                            print(f"✅ Autor {curp} procesado correctamente.")
            except Exception as e:
                errores.append({
                    "fila": int(index) + int(header_row) + 2,
                    "curp": curp,
                    "error": str(e)
                })
                print(f"❌ Error en autor {curp}: {e}")

        print(f"📗 Autores procesados: {creados} | Errores: {len(errores)}")
        return creados, errores

    # ==========================================================
    # 🧾 2️⃣ CARGA DE REGISTROS IMPI
    # ==========================================================
    def _procesar_registros(self, xls, id_usuario, hojas_input):
        hojas_disponibles = [h for h in xls.sheet_names if h.isdigit()]
        hojas_a_cargar = self._parse_hojas(hojas_input, hojas_disponibles)
        creados, actualizados, errores = 0, 0, []

        for hoja in hojas_a_cargar:
            print(f"📘 Procesando hoja IMPI: {hoja}")
            preview = pd.read_excel(xls, sheet_name=hoja, nrows=6, header=None)
            header_row = next(
                (i for i, row in preview.iterrows()
                 if any(str(c).strip().startswith("N. Expediente") for c in row)), 4
            )

            df = pd.read_excel(xls, sheet_name=hoja, header=header_row)
            df = df.dropna(how="all")
            df = df[df["N. Expediente (1)"].notna()]

            for index, row in df.iterrows():
                expediente = str(row.get("N. Expediente (1)", "")).strip()
                if not expediente or expediente.lower() == "nan":
                    continue

                try:
                    fec_solicitud = pd.to_datetime(row.get("Fecha de Solicitud (4)"), errors="coerce")
                    fec_expedicion = pd.to_datetime(row.get("Fecha de Expedición (15)"), errors="coerce")

                    with transaction.atomic():
                        registro_data = {
                            "no_expediente": expediente,
                            "titulo": str(row.get("Denominación (3)", "")).strip() or None,
                            "descripcion": str(row.get("Descripción (18)", "")).strip() or None,
                            "fec_solicitud": fec_solicitud if pd.notna(fec_solicitud) else None,
                            "no_titulo": str(row.get("N. De Título (2)", "")).strip() or None,

                            "estatus_param": self._resolve_param_mixto(row.get("Estatus (6)"), self.temas["Estatus"]),
                            "rama_param": self._resolve_param_mixto(row.get("Rama (5)"), self.temas["Rama"]),
                            "medio_ingreso_param": self._resolve_param_mixto(row.get("Medio de Ingreso (7)"), self.temas["Medio de Ingreso"]),

                            "tipo_ingreso_param": 44,
                            "tipo_registro_param": 44,

                            "institucion_id": self._resolve_institucion_id(row.get("Tecnologico de Origen (8)")),
                            "cepat_id": self._resolve_cepat_id(row.get("CePat (9)") or row.get("CEPAT (9)")),

                            "anio_renovacion": self._to_int(row.get("Año Renovación (10)")),
                            "sector_param": self._resolve_param_mixto(row.get("Sector (12)"), self.temas["Sector"]),
                            "id_subsector": self._to_int(row.get("Subsector (13)")),
                            "fec_expedicion": fec_expedicion if pd.notna(fec_expedicion) else None,
                            "archivo": str(row.get("Archivo (16)", "")).strip(),
                            "observaciones": str(row.get("Observaciones (17)", "")).strip(),
                            "id_usuario": id_usuario,
                        }

                        registro_existente = self.registros_repo.get_by_expediente(expediente)
                        if registro_existente:
                            actualizados += 1
                            continue

                        create_new_record(registro_data)
                        creados += 1

                        inventores = str(row.get("Inventores (14)", "")).strip()
                        if not inventores:
                            continue

                        curps = [c.strip() for c in inventores.split(",") if c.strip()]
                        curps = list(dict.fromkeys(curps))  # eliminar duplicados
                        for curp in curps:
                            investigador_existente = self.investigadores_repo.get_by_curp(curp)
                            if investigador_existente:
                                add_investigador_to_registro(curp, investigador_existente, expediente)
                            else:
                                print(f"⚠️ Investigador {curp} no encontrado (verifica hoja 'AUTORES').")

                except Exception as e:
                    errores.append({
                        "hoja": hoja,
                        "fila": int(index) + int(header_row) + 2,
                        "expediente": expediente,
                        "error": str(e)
                    })
                    print(f"❌ Error en registro {expediente}: {e}")

        print(f"📘 Registros IMPI creados: {creados} | Actualizados: {actualizados} | Errores: {len(errores)}")
        return creados, actualizados, errores

    # ==========================================================
    # 🧩 UTILIDADES Y CONVERSORES
    # ==========================================================
    def _resolve_param_mixto(self, valor, id_tema):
        if valor is None or pd.isna(valor):
            return None
        try:
            return int(valor)
        except (ValueError, TypeError):
            valor = str(valor).strip()
            if not valor:
                return None
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_param
                    FROM parametrizacion
                    WHERE LOWER(nombre) = LOWER(%s)
                      AND id_tema = %s
                    LIMIT 1;
                """, [valor, id_tema])
                row = cursor.fetchone()
                return row[0] if row else None

    def _resolve_institucion_id(self, nombre: str):
        if not nombre or pd.isna(nombre):
            return None
        nombre = str(nombre).strip()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_institucion
                FROM institucion
                WHERE LOWER(nombre) = LOWER(%s)
                LIMIT 1;
            """, [nombre])
            row = cursor.fetchone()
            return row[0] if row else None

    def _resolve_cepat_id(self, nombre: str):
        if not nombre or pd.isna(nombre):
            return None
        nombre = str(nombre).strip()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_cepat
                FROM cepat
                WHERE LOWER(nombre) = LOWER(%s)
                LIMIT 1;
            """, [nombre])
            row = cursor.fetchone()
            return row[0] if row else None

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
