from apps.registros.domain.entities import Registro
from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository

repo = PostgresRegistroRepository()

def create_new_record(data: dict) -> dict:
    valid_fields = {
        "no_expediente","titulo","descripcion","fec_solicitud","no_titulo",
        "estatus_param","rama_param","medio_ingreso_param","tecnologico_origen",
        "anio_renovacion","id_subsector","fec_expedicion","archivo","observaciones",
        "tipo_registro_param","tipo_ingreso_param","id_usuario"
    }
    clean = {k: data.get(k) for k in valid_fields}
    reg = Registro(**clean)
    saved = repo.upsert(reg)
    return {"created": saved.get("created", True), **saved}
