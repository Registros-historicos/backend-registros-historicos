from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository

def list_records(tipo_registro_param: int, page: int = 1, limit: int = 10, filter: str = "fecha_solicitud", order: str = "asc", id_usuario: int = None) -> dict:
    """ 
    Lista registros paginados por tipo.
    Retorna: {'total': int, 'page': int, 'limit': int, 'results': list[dict]}
    """

    repository = PostgresRegistroRepository()
    offset = (page - 1) * limit

    total = repository.contar_por_tipo(tipo_registro_param, id_usuario)
    results = repository.listar_por_tipo(tipo_registro_param, limit, offset, filter, order, id_usuario)

    return {
        'total': total,
        'page': page,
        'limit': limit,
        'results': results
    }
