from abc import ABC, abstractmethod
from typing import Iterable, Optional
from .entities import Usuario

class UserRepositoryPort(ABC):

    @abstractmethod
    def create(self, user: Usuario, pwd_hash: str) -> int: ...

    @abstractmethod
    def update(self, user_id: int, user: Usuario, pwd_hash: Optional[str] = None) -> None: ...

    @abstractmethod
    def delete(self, user_id: int) -> None: ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[Usuario]: ...

    @abstractmethod
    def list(self, q: str = "", estatus: Optional[int] = None,
             limit: int = 50, offset: int = 0) -> Iterable[Usuario]: ...
