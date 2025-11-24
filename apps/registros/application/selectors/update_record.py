from apps.registros.domain.entities import Registro
from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository
from dataclasses import fields

def update_records(id_registro: int, data: dict) -> Registro:
    """
    Actualiza un registro:
    - Lee el registro actual desde PostgreSQL.
    - Fusiona los datos actuales con los nuevos del request.
    - Filtra solo los campos que pertenecen al dataclass Registro.
    - Llama al repositorio para ejecutar la función f_actualiza_resgistro_por_pk.
    """
    repo = PostgresRegistroRepository()

    # 1) Obtener los datos actuales desde la BD (dict con muchos campos)
    actual = repo.obtener_por_id(id_registro)
    if actual is None:
        raise ValueError(f"El registro con id {id_registro} no existe")

    # 2) Fusionar: lo nuevo del request pisa a lo viejo del registro actual
    merged = {**actual, **data}

    # 3) Quedarnos solo con los campos definidos en el dataclass Registro
    campos_registro = {f.name for f in fields(Registro)}
    cleaned = {k: v for k, v in merged.items() if k in campos_registro}

    # 4) Crear la entidad de dominio Registro a partir de los datos filtrados
    registro = Registro(**cleaned)

    # 5) Delegar la actualización al repositorio (que llama a la función SQL)
    return repo.actualizar(id_registro, registro)

