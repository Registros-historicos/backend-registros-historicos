from apps.consultas.infrastructure.repositories.records_by_period_repo import RecordsByPeriodRepository

def registros_por_periodo_selector(fecha_inicio: str, fecha_fin: str):
    """
    Retorna los registros agrupados por año, mes y tipo de registro.
    """
    repo = RecordsByPeriodRepository()
    datos = repo.obtener_registros_por_periodo(fecha_inicio, fecha_fin)
    datos_ordenados = sorted(datos, key=lambda x: (x["anio"], x["mes"]))
    return datos_ordenados
