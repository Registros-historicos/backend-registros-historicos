from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.consultas.application.selectors.export_excel import dataframe_to_styled_excel_bytes, \
    dataframe_to_excel_registros_mes
from apps.consultas.application.selectors.requests_by_type_queries import requests_impi, requests_indautor, \
    requests_by_type_selector
from apps.consultas.application.selectors.institutions_top10_queries import instituciones_top10
from apps.consultas.application.selectors.category_researchers import conteo_investigadores_por_categoria_selector
from apps.consultas.application.selectors.federal_entities_top10_queries import entidades_top10
from apps.consultas.application.selectors.records_by_status import conteo_registros_por_estatus_selector
from apps.consultas.application.selectors.economic_sectors_queries import conteo_registros_por_sector_selector
from apps.consultas.application.selectors.records_by_sex_queries import registros_por_sexo_selector
from apps.consultas.application.selectors.institutions_all_queries import instituciones_all
from apps.consultas.application.selectors.federal_entities_all_queries import entidades_all
from apps.consultas.application.selectors.sectors_activity_queries import sectores_actividad_top10
from apps.consultas.application.selectors.records_by_month_queries import registros_por_mes_selector
from apps.consultas.application.selectors.records_by_period import registros_por_periodo_selector
from apps.consultas.application.selectors.institutions_filtered_queries import instituciones_filtradas_selector
from apps.consultas.application.selectors.investigador_por_coordinador import investigadores_por_coordinador_selector
from apps.consultas.application.selectors.usuarios_por_estados_cepat import usuarios_por_estados_cepat_selector
from apps.consultas.application.selectors.programs_educational_queries import registros_por_programa_educativo_selector
from apps.consultas.application.selectors.registros_por_programa_selector import registros_por_programa_selector
from apps.consultas.application.selectors.coordinadores_por_cepat_selector import coordinadores_por_cepat_selector
from apps.consultas.infrastructure.web.serializer import (
    EntidadTopSerializer,
    CategoriaInvestigadorSerializer,
    InstitucionTopSerializer,
    SectorEconomicoSerializer,
    RegistrosPorSexoSerializer,
    RequestTypeSerializer,
    SectorActividadSerializer,
    RegistrosPorMesSerializer,
    RegistrosPorPeriodoSerializer,
    InstitucionAllSerializer,
    InvestigadorPorCoordinadorSerializer,
    UsuarioPorEstadoCepatSerializer,
    ProgramaEducativoSerializer,
    RegistrosPorProgramaSerializer,
    CoordinadorConInstitucionSerializer
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.users.application.services.permissions import HasRole
import pandas as pd
from django.http import FileResponse


class ConsultaViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, HasRole]
    allowed_roles = [35, 36, 37]  # Permite acceso a Administrador (35), Coordinador (36) y CEPAT (37)
    """
    ViewSet para tableros de consultas.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @extend_schema(
        summary="Top 10 entidades federativas por número de registros",
        responses={200: EntidadTopSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def entidades_top10_view(self, request):
        resultado = entidades_top10()
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Mostrar registros agrupados por estatus (Confirmada, Pendiente, Rechazada)",
        responses={200: EntidadTopSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def records_by_status_view(self, request):
        resultado = conteo_registros_por_estatus_selector(request.user)
        return Response(resultado, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def categoria_investigadores_view(self, request):
        resultado = conteo_investigadores_por_categoria_selector(request.user)
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Top 10 instituciones por número de registros",
        responses={200: InstitucionTopSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def instituciones_top10_view(self, request):
        resultado = instituciones_top10(user=request.user)
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Registros agrupados por sector económico",
        responses={200: SectorEconomicoSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def registros_por_sector_view(self, request):
        resultado = conteo_registros_por_sector_selector()
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Conteo de registros por sexo de investigador",
        responses={200: RegistrosPorSexoSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def registros_por_sexo_view(self, request):
        resultado = registros_por_sexo_selector(request.user)
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Requests grouped by type (IMPI)",
        responses={200: RequestTypeSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def requests_impi_view(self, request):
        result = requests_by_type_selector(44, request.user)  # 44 = tipo IMPI
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Requests grouped by type (INDAUTOR)",
        responses={200: RequestTypeSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def requests_indautor_view(self, request):
        result = requests_by_type_selector(45, request.user)  # 45 = tipo INDAUTOR
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Todas las instituciones con número de registros",
        responses={200: InstitucionAllSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def instituciones_all_view(self, request):
        resultado = instituciones_all(user=request.user)
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Todas las entidades federativas con número de registros",
        responses={200: EntidadTopSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def entidades_all_view(self, request):
        resultado = entidades_all()
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Top 10 registros agrupados por sector/actividad económica",
        responses={200: SectorActividadSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def sectores_actividad_view(self, request):
        resultado = sectores_actividad_top10()
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Todos los registros agrupados por sector/actividad económica",
        responses={200: SectorActividadSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def sectores_actividad_all_view(self, request):
        from apps.consultas.application.selectors.sectors_activity_all_selector import sectores_actividad_all
        resultado = sectores_actividad_all(request.user)
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Conteo de registros por mes para un año específico",
        parameters=[
            OpenApiParameter(
                name='anio',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Año para filtrar los registros (ej: 2024)',
                required=True
            )
        ],
        responses={200: RegistrosPorMesSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def registros_por_mes_view(self, request):
        anio = request.query_params.get('anio')

        if not anio:
            return Response(
                {"error": "El parámetro 'anio' es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            anio = int(anio)
        except ValueError:
            return Response(
                {"error": "El parámetro 'anio' debe ser un número entero"},
                status=status.HTTP_400_BAD_REQUEST
            )

        resultado = registros_por_mes_selector(anio, request.user)
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Conteo de registros agrupados por año, mes y tipo de registro",
        parameters=[
            OpenApiParameter(
                name='inicio',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Fecha de inicio del rango (YYYY-MM-DD)',
                required=True
            ),
            OpenApiParameter(
                name='fin',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Fecha de fin del rango (YYYY-MM-DD)',
                required=True
            ),
            OpenApiParameter(
                name='fin',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Fecha de fin del rango (YYYY-MM-DD)',
                required=True
            )
        ],
        responses={200: RegistrosPorPeriodoSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def registros_por_periodo(self, request):
        """
        Endpoint para obtener registros agrupados por año, mes y tipo de registro
        dentro de un rango de fechas.
        """
        fecha_inicio = request.query_params.get('inicio')
        fecha_fin = request.query_params.get('fin')

        if not fecha_inicio or not fecha_fin:
            return Response(
                {"error": "Debe enviar los parámetros 'inicio' y 'fin' (YYYY-MM-DD)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            resultado = registros_por_periodo_selector(fecha_inicio, fecha_fin, request.user)
            serializer = RegistrosPorPeriodoSerializer(resultado, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Instituciones filtradas por tipo (Federal/Descentralizado)",
        parameters=[
            OpenApiParameter(
                name='tipo_institucion',
                type=int,
                location=OpenApiParameter.QUERY,
                description='ID del tipo de institución (ej: 122=Descentralizado, 123=Federal)',
                required=True
            )
        ],
        responses={200: InstitucionTopSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def instituciones_filtradas_view(self, request):
        tipo_institucion = request.query_params.get('tipo_institucion')

        if not tipo_institucion:
            return Response(
                {"error": "El parámetro 'tipo_institucion' es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            tipo_institucion = int(tipo_institucion)
        except ValueError:
            return Response(
                {"error": "El parámetro 'tipo_institucion' debe ser un número entero"},
                status=status.HTTP_400_BAD_REQUEST
            )
        resultado = instituciones_filtradas_selector(tipo_institucion)
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="[Coordinador] Lista los investigadores de la institución del coordinador",
        responses={200: InvestigadorPorCoordinadorSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def investigadores_por_coordinador_view(self, request):
        """
        Endpoint que retorna los investigadores asociados a la(s) institución(es)
        del usuario coordinador que realiza la petición.
        """
        # Llama al selector pasándole el usuario autenticado
        resultado = investigadores_por_coordinador_selector(request.user)
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="[CEPAT] Obtener usuarios coordinadores en los estados del CEPAT",
        description="Devuelve la info completa de usuarios cuyas instituciones están en los mismos estados que gestiona el CEPAT logueado.",
        responses={200: UsuarioPorEstadoCepatSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def usuarios_por_estados_cepat_view(self, request):
        resultado = usuarios_por_estados_cepat_selector(request.user)
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Conteo de registros por programa educativo",
        responses={200: ProgramaEducativoSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def programas_educativos_view(self, request):
        resultado = registros_por_programa_educativo_selector(request.user)
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="[Coordinador] Conteo de registros por Programa Educativo",
        description="Devuelve la cantidad de registros agrupados por el programa educativo de la institución del coordinador.",
        responses={200: RegistrosPorProgramaSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def registros_por_programa_view(self, request):
        resultado = registros_por_programa_selector(request.user)
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="[CEPAT] Obtener coordinadores asociados",
        description="Obtiene lista de coordinadores (usuarios) que pertenecen a las instituciones del CEPAT en sesión.",
        responses={200: CoordinadorConInstitucionSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def coordinadores_por_cepat_view(self, request):
        resultado = coordinadores_por_cepat_selector(request.user)
        return Response(resultado, status=status.HTTP_200_OK)


class ConsultaExcelViewSet(viewsets.ViewSet):
    """
    ViewSet para tableros de consultas.
    """
    allowed_roles = [35, 36, 37]

    def _generar_respuesta_excel(
            self,
            data_list,
            mapping,
            sheet_name,
            table_name,
            file_name,
            report_title=None,
            add_pie_chart=False,
            chart_labels_col_idx=1,
            chart_data_col_idx=2
    ):
        try:
            # 1. Normalización de datos (Igual que antes)
            if hasattr(data_list, "data"):
                data = data_list.data
            else:
                data = data_list

            rows = []
            if isinstance(data, dict) and "data" in data:
                rows = data["data"]
            elif isinstance(data, (list, tuple)):
                rows = data
            elif isinstance(data, dict):
                rows = [data]

            # 2. DataFrame y Filtrado (Igual que antes)
            if rows:
                df = pd.DataFrame(rows)
            else:
                df = pd.DataFrame([{"Info": "Sin resultados"}])

            cols = [c for c in mapping.keys() if c in df.columns]
            if cols: df = df[cols]

            # 3. Generar Excel PASANDO LOS NUEVOS PARÁMETROS
            excel_io = dataframe_to_styled_excel_bytes(
                df,
                sheet_name=sheet_name,
                table_name=table_name,
                column_mapping=mapping,
                report_title=report_title,
                add_pie_chart=add_pie_chart,
                chart_labels_col_idx=chart_labels_col_idx,
                chart_data_col_idx=chart_data_col_idx
            )

            response = FileResponse(excel_io, as_attachment=True, filename=file_name)
            response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            return response

        except Exception as e:
            print(f"Error generando Excel {file_name}: {str(e)}")
            return Response({"error": str(e)}, status=500)


    @action(detail=False, methods=["get"])
    def entidades_top10_excel(self, request):
        data = entidades_top10()
        mapping = {
            "entidad_nombre": "Entidad",
            "total": "Total de registros"
        }
        return self._generar_respuesta_excel(
            data_list=data,
            mapping=mapping,
            sheet_name="TopEntidades",
            table_name="TablaEntidades",
            file_name="reporte_entidades.xlsx",
            report_title="Top 10 Entidades Federativas"
        )

    @action(detail=False, methods=["get"])
    def institutos_top10_excel(self, request):
        data = instituciones_top10()
        mapping = {
            "institucion_nombre": "Institución",
            "total": "Total de registros"
        }
        return self._generar_respuesta_excel(
            data_list=data,
            mapping=mapping,
            sheet_name="TopInstitutos",
            table_name="TablaInstitutos",
            file_name="reporte_top10_instituciones.xlsx",
            report_title="TOP 10 INSTITUCIONES CON MÁS REGISTROS"
        )


    @action(detail=False, methods=["get"])
    def institutos_descentralizados_excel(self, request):
        data = instituciones_filtradas_selector(tipo_institucion=123)

        mapping = {
            "institucion_nombre": "Institución",
            "total": "Total de registros"
        }

        return self._generar_respuesta_excel(
            data_list=data,
            mapping=mapping,
            sheet_name="Institutos Descentralizados",
            table_name="TablaDescentralizados",
            file_name="reporte_institutos_descentralizados.xlsx",
            report_title="INSTITUCIONES DESCENTRALIZADAS CON MÁS REGISTROS"
        )

    @action(detail=False, methods=["get"])
    def institutos_federales_excel(self, request):
        data = instituciones_filtradas_selector(tipo_institucion=122)

        mapping = {
            "institucion_nombre": "Institución",
            "total": "Total de registros"
        }

        return self._generar_respuesta_excel(
            data_list=data,
            mapping=mapping,
            sheet_name="Institutos Federales",
            table_name="TablaFederales",
            file_name="reporte_institutos_federales.xlsx",
            report_title="INSTITUCIONES FEDERALES CON MÁS REGISTROS"
        )

    @action(detail=False, methods=["get"])
    def all_institutos_excel(self, request):
        data = instituciones_all(user=request.user)

        mapping = {
            "institucion_nombre": "Institución",
            "total": "Total de registros"
        }

        return self._generar_respuesta_excel(
            data_list=data,
            mapping=mapping,
            sheet_name="Todos los Institutos",
            table_name="TablaInstitutos",
            file_name="reporte_todos_los_institutos.xlsx",
            report_title="TODAS LAS INSTITUCIONES CON REGISTROS"
        )

    @action(detail=False, methods=["get"])
    def sectores_economicos_excel(self, request):
        from apps.consultas.application.selectors.sectors_activity_all_selector import sectores_actividad_all
        data = sectores_actividad_all(request.user)

        mapping = {
            "actividad_nombre": "Sectores Económicos",
            "sector_nombre": "Tipo de Sector",
            "total": "Total de registros"
        }

        return self._generar_respuesta_excel(
            data_list=data,
            mapping=mapping,
            sheet_name="Sectores Económicos",
            table_name="TablaSectores",
            file_name="reporte_sectores_economicos.xlsx",
            report_title="SECTORES ECONÓMICOS CON MÁS REGISTROS"
        )

    @action(detail=False, methods=["get"])
    def registros_impi_excel(self, request):
        data = requests_by_type_selector(44, request.user)  # 44 = tipo IMPI
        mapping = {
            "tipo_registro_nombre": "Tipo de Registro",
            "rama_nombre": "Nombre de la Rama",
            "total": "Total de Solicitudes"
        }
        return self._generar_respuesta_excel(
            data_list=data,
            mapping=mapping,
            sheet_name="IMPI",
            table_name="TablaIMPI",
            file_name="reporte_impi_.xlsx",
            report_title="REGISTROS IMPI",
            add_pie_chart=True,
            chart_labels_col_idx=2,
            chart_data_col_idx=3
        )

    @action(detail=False, methods=["get"])
    def registros_indautor_excel(self, request):
        data = requests_by_type_selector(45, request.user)
        mapping = {
            "tipo_registro_nombre": "Tipo de Registro",
            "rama_nombre": "Nombre de la Rama",
            "total": "Total de Solicitudes"
        }
        return self._generar_respuesta_excel(
            data_list=data,
            mapping=mapping,
            sheet_name="INDAUTOR",
            table_name="TablaINDAUTOR",
            file_name="reporte_indautor.xlsx",
            report_title="REGISTROS INDAUTOR",
            add_pie_chart=True,
            chart_labels_col_idx=2,
            chart_data_col_idx=3
        )

    @action(detail=False, methods=["get"])
    def categorias_excel(self, request):
        data = conteo_investigadores_por_categoria_selector(request.user)
        mapping = {
            "categoria": "Registros por categoría",
            "total": "Total"
        }
        return self._generar_respuesta_excel(
            data_list=data,
            mapping=mapping,
            sheet_name="Ceategorías",
            table_name="TablaCategorías",
            file_name="reporte_categorias.xlsx",
            report_title="REGISTROS POR CATEGORÍA DE INVESTIGADOR",
            add_pie_chart=True,
            chart_labels_col_idx=1,
            chart_data_col_idx=2
        )

    @action(detail=False, methods=["get"])
    def sexos_excel(self, request):
        data =  registros_por_sexo_selector(request.user)
        mapping = {
            "sexo": "Registros por sexo",
            "total": "Total"
        }
        return self._generar_respuesta_excel(
            data_list=data,
            mapping=mapping,
            sheet_name="Sexo",
            table_name="TablaSexo",
            file_name="reporte_investigadores_por_sexo.xlsx",
            report_title="REGISTROS DE INVESTIGADORES POR SEXO",
            add_pie_chart=True,
            chart_labels_col_idx=1,
            chart_data_col_idx=2
        )

    @action(detail=False, methods=["get"])
    def registros_estatus_excel(self, request):
        data = conteo_registros_por_estatus_selector(request.user)
        mapping = {
            "estatus": "Estatus actual",
            "total": "Total"
        }
        return self._generar_respuesta_excel(
            data_list=data,
            mapping=mapping,
            sheet_name="Estatus",
            table_name="TablaEstatus",
            file_name="reporte_estatus_registros.xlsx",
            report_title="REPORTE DE REGISTROS POR ESTATUS",
            add_pie_chart=True,
            chart_labels_col_idx=1,
            chart_data_col_idx=2
        )

    @action(detail=False, methods=["get"])
    def registros_por_mes_excel(self, request):
        year = request.query_params.get("anio")

        if not year:
            return Response({"error": "El parámetro 'anio' es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            year = int(year)
        except ValueError:
            return Response({"error": "El parámetro 'anio' debe ser un número entero"},
                            status=status.HTTP_400_BAD_REQUEST)

        raw_data = registros_por_mes_selector(year, request.user)

        meses_map = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
            7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
        }
        processed_data = []
        conteo_por_mes = {}

        for item in raw_data:
            mes_num = item.get("mes")
            nombre_mes = meses_map.get(mes_num, "Desconocido")

            veces_visto = conteo_por_mes.get(mes_num, 0)
            fuente = "IMPI" if veces_visto == 0 else "Indautor"
            conteo_por_mes[mes_num] = veces_visto + 1

            processed_data.append({
                "concepto": f"{nombre_mes} - {fuente}",
                "total": item.get("total")
            })

        if processed_data:
            df = pd.DataFrame(processed_data)
        else:
            df = pd.DataFrame([{"concepto": "Sin datos", "total": 0}])

        df = df.rename(columns={
            "concepto": "Mes / Fuente",
            "total": "Total Registros"
        })
        file_name = f"reporte_registros_por_mes_{year}.xlsx"
        try:
            excel_io = dataframe_to_excel_registros_mes(
                df,
                sheet_name=f"Registros {year}",
                table_name=f"TablaRegistros{year}",
                report_title=f"REPORTE DE REGISTROS POR MES - {year}",
                chart_labels_col_idx=1,
                chart_data_col_idx=2
            )

            response = FileResponse(excel_io, as_attachment=True, filename=file_name)
            response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=500)