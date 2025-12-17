
from apps.investigadores.infrastructure.repositories.investigadores_repositorio import PostgresInvestigadorRepository

repo_investigador = PostgresInvestigadorRepository()


class ListInvestigadorService:
    """
    Servicio de aplicación para listar investigadores.
    """

    def list_all(self):
        """Obtiene todos los investigadores."""
        investigadores = repo_investigador.list_all()
        return investigadores

    def list_curps(self):
        """Obtiene todas las CURP de investigadores."""
        curps = repo_investigador.list_curps()
        return curps