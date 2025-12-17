from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository
from apps.registros.infrastructure.repositories.investigadores_repositorio import PostgresInvestigadorRepository

repo_registro = PostgresRegistroRepository()
repo_investigador = PostgresInvestigadorRepository()


def add_investigador_to_registro(curp: str, investigador_data: dict, no_expediente: str):
    """
    Vincula un investigador existente (por CURP) a un registro,
    usando su id_investigador en la tabla registro_investigador.
    
    Args:
        curp: CURP del investigador a vincular
        investigador_data: Datos adicionales del investigador (opcional, para compatibilidad)
        no_expediente: Número de expediente del registro
        
    Returns:
        dict: Diccionario con información de la vinculación exitosa
        None: Si no se encontró el investigador o el registro
    """
    # Buscar investigador por CURP
    investigador = repo_investigador.get_by_curp(curp)
    if not investigador:
        print(f"⚠️ CURP {curp} no encontrado, se omite vinculación.")
        return None

    # Buscar registro por expediente
    registro = repo_registro.get_by_expediente(no_expediente)
    if not registro:
        print(f"⚠️ Registro con expediente {no_expediente} no encontrado.")
        return None

    # Obtener IDs para la vinculación
    id_investigador = investigador["id_investigador"]
    id_registro = registro["id_registro"]
    
    # Vincular investigador al registro
    repo_registro.vincular_investigador(id_registro, id_investigador)
    print(f"✅ Vinculado investigador {id_investigador} → registro {id_registro}")
    
    # Retornar información de la vinculación exitosa
    return {
        "success": True,
        "message": "Investigador vinculado exitosamente",
        "data": {
            "id_investigador": id_investigador,
            "id_registro": id_registro,
            "curp": curp,
            "no_expediente": no_expediente,
            "investigador": {
                "nombre": investigador.get("nombre"),
                "apellido_paterno": investigador.get("apellido_paterno"),
                "apellido_materno": investigador.get("apellido_materno")
            }
        }
    }