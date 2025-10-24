from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository

def search_records(tipo_registro_param: int, texto: str, page: int, limit: int, filter: dict, order: dict) -> dict:
    """ 
    Busca registros por texto con paginación.
    Retorna: {'total': int, 'page': int, 'limit': int, 'results': list[dict]}
    """

    repository = PostgresRegistroRepository()
    offset = (page - 1) * limit
    print(offset)

    total = repository.contar_por_texto(tipo_registro_param, texto)
    results = repository.listar_por_tipo(tipo_registro_param, limit, offset, filter, order)

    return {
        'total': total,
        'page': page,
        'limit': limit,
        'results': results
    }