from apps.investigadores.domain.ports import InvestigadorRepositoryPort


class DeleteInvestigadorService:
    """
    Servicio de aplicación para eliminar un investigador.
    """

    def __init__(self, repo: InvestigadorRepositoryPort):
        self.repo = repo

    def execute(self, id_investigador: int) -> None:
        """
        Ejecuta la eliminación del investigador usando la función Postgres f_eliminar_investigador.
        """
        self.repo.eliminar(id_investigador)
