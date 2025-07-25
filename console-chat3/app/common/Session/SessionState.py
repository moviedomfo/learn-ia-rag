from multiprocessing import Lock
from app.common.Session.SocioBE import SocioBE
from app.common.Session.UsersRepository import UsersRepository
from app.common.Session.UsersRepositorySingleton import UsersRepositorySingleton


# 3.  Estado de chat (ligero): usa Socio + historial para RAG
class SessionState:
    __repo_lock = Lock()
         
    socio:SocioBE
    def __init__(self, phone: str,users_repo: UsersRepository = UsersRepository()):
        self.phone = phone
        self.users_repo = users_repo  # siempre retorna la misma instancia

        with SessionState.__repo_lock:

             # ── Rescatamos (o creamos) el socio asociado ──
            self.socio:SocioBE = self.users_repo.get_by_phone(phone)
            if self.socio is None:
                self.socio = SocioBE(phone=phone)
                self.users_repo.persist(self.socio)

    

    def persist_socio(self) -> None:
        self.users_repo.persist(self.socio)
      

    def has_socio(self,phone:str) -> SocioBE | None:
        return self.users_repo.get_by_phone(phone)
    

