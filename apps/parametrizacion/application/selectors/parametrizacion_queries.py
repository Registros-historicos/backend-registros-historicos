from apps.parametrizacion.infrastructure.repositories.parametrizacion_repo import ParametrizacionRepository

def get_all_parametrizaciones():
    repo = ParametrizacionRepository()
    return repo.get_all()

def get_parametrizaciones_by_tema(id_tema: int):
    repo = ParametrizacionRepository()
    return repo.get_by_tema(id_tema)
