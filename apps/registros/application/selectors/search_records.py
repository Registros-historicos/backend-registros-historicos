from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository

def search_records(tipo_registro_param: int, texto: str, page: int, limit: int) -> dict:
    """ 
    Busca registros por texto con paginación.
    Retorna: {'total': int, 'page': int, 'limit': int, 'results': list[dict]}
    """

    repository = PostgresRegistroRepository()
    offset = (page - 1) * limit
    print(offset)

    total = repository.contar_por_texto(tipo_registro_param, texto)
    results = repository.buscar_por_texto(tipo_registro_param, texto, limit, offset)

    return {
        'total': total,
        'page': page,
        'limit': limit,
        'results': results
    }