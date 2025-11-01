from apps.investigadores.domain.entities import Adscripcion
from apps.investigadores.domain.ports import InvestigadorRepositoryPort
from datetime import date

class CreateAdscripcionService:
    def __init__(self, repo: InvestigadorRepositoryPort):
        self.repo = repo

    def execute(
        self,
        id_investigador,
        id_institucion,
        departamento_param,
        programa_educativo_param,
        cuerpo_academico_param,
        fec_ini,
        fec_fin=None
    ):
        adscripcion = Adscripcion(
            id_adscripcion=None,
            id_investigador=id_investigador,
            id_institucion=id_institucion,
            departamento_param=departamento_param,
            programa_educativo_param=programa_educativo_param,
            cuerpo_academico_param=cuerpo_academico_param,
            fec_ini=fec_ini,
            fec_fin=fec_fin
        )
        return self.repo.crear_adscripcion(adscripcion)
