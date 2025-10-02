from typing import Optional, Iterable
from apps.users.domain.entities import Usuario
from apps.users.domain.ports import UserRepositoryPort

class UserQueriesSelector:
    def __init__(self, repo: UserRepositoryPort):
        self.repo = repo

    def get(self, user_id: int) -> Optional[Usuario]:
        return self.repo.get_by_id(user_id)

    def list(self, q: str = "", estatus: Optional[int] = None, limit: int = 50, offset: int = 0) -> Iterable[Usuario]:
        return self.repo.list(q=q, estatus=estatus, limit=limit, offset=offset)
