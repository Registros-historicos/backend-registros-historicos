from apps.investigadores.domain.entities import Investigador

class CreateInvestigadorService:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, nombre, ape_pat, ape_mat, curp, sexo_param, tipo_investigador_param):

        investigador = Investigador(
            id_investigador=None,   # importa si tu función lo genera
            nombre=nombre,
            ape_pat=ape_pat,
            ape_mat=ape_mat,
            curp=curp,
            sexo_param=sexo_param,
            tipo_investigador_param=tipo_investigador_param
        )

        return self.repo.crear(investigador)
