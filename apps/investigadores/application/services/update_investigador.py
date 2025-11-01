from apps.investigadores.domain.entities import Investigador
from apps.investigadores.domain.ports import InvestigadorRepositoryPort


class UpdateInvestigadorService:
    """
    Servicio de aplicación para actualizar los datos de un investigador.
    """

    def __init__(self, repo: InvestigadorRepositoryPort):
        self.repo = repo

    def execute(
        self,
        id_investigador: int,
        nombre: str,
        apellido_paterno: str,
        apellido_materno: str,
        correo: str,
        curp: str,
    ) -> None:
        """
        Ejecuta la actualización del investigador.
        """
        investigador = Investigador(
            id_investigador=id_investigador,
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            correo=correo,
            curp=curp,
        )

        self.repo.actualizar(investigador)
