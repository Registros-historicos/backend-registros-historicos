from apps.registros.domain.entities import Registro

class RegistroService:
    def __init__(self, repo):
        self.repo = repo

    def crear_registro(self, data):
        registro = Registro(**data)
        return self.repo.insertar(registro)

    def actualizar_registro(self, id_registro, data):
        registro = Registro(**data)
        return self.repo.actualizar(id_registro, registro)

    def habilitar_registro(self, id_registro):
        self.repo.habilitar(id_registro)

    def deshabilitar_registro(self, id_registro):
        self.repo.deshabilitar(id_registro)
