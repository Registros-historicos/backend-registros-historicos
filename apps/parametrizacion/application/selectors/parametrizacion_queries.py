from apps.parametrizacion.infrastructure.repositories.parametrizacion_repo import ParametrizacionRepository

def get_all_parametrizaciones():
    repo = ParametrizacionRepository()
    return repo.get_all()

def get_parametrizaciones_by_tema(id_tema: int):
    repo = ParametrizacionRepository()
    return repo.get_by_tema(id_tema)

def get_estado_param():
    repo = ParametrizacionRepository()
    return repo.get_estados()

def get_instituciones_por_estado(id_entidad_federativa: int):
    repo = ParametrizacionRepository()
    return repo.get_instituciones_por_estado(id_entidad_federativa)
