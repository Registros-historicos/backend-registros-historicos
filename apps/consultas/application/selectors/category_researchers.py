from apps.consultas.infrastructure.repositories.category_researchers_repo import RegistroRepositorio

def conteo_investigadores_por_categoria_selector() -> list[dict]:
    repositorio = RegistroRepositorio()
    return repositorio.obtener_conteo_por_tipo_investigador()
