
# Aquí se definen las excepciones personalizadas para el core del sistema

class CoreException(Exception):
    """Excepción base para el core del sistema."""
    pass


class ServiceError(CoreException):
    """Error en la capa de aplicación/servicios."""
    def __init__(self, message="Ocurrió un error en el servicio", code=None):
        self.message = message
        self.code = code
        super().__init__(self.message)


class DomainError(CoreException):
    """Error en la capa de dominio (reglas de negocio)."""
    def __init__(self, message="Error en la lógica de negocio"):
        self.message = message
        super().__init__(self.message)
