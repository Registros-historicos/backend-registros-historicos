from apps.consultas.infrastructure.repositories.category_researchers_repo import RegistroRepositorio
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def conteo_investigadores_por_categoria_selector(user) -> list[dict]:
    id_usuario = getattr(user, "id", None)
    
    context = resolve_user_context(int(id_usuario))
    if not context:
        return []
    
    rol_id = context["rol_id"]
    id_cepat = context.get("id_cepat")
    id_institucion = context.get("id_institucion")
    
    repositorio = RegistroRepositorio()
    
    if rol_id == 35:
        return repositorio.obtener_conteo_global()
    elif rol_id == 37:
        return repositorio.obtener_conteo_por_cepat(id_cepat)
    elif rol_id == 36:
        return repositorio.obtener_conteo_por_institucion(id_institucion)
    else:
        print("Usuario otro rol detectado, id_usuario:", id_usuario)
        return []
