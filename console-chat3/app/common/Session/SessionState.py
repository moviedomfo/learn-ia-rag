from multiprocessing import Lock
from app.common.Session.SocioBE import SocioBE
from app.common.Session.UsersRepository import UsersRepository


# 3.  Estado de chat (ligero): usa Socio + historial para RAG
class SessionState:
    _repo_lock = Lock()

    _repo = UsersRepository()        # compartido
    socio:SocioBE
    def __init__(self, phone: str):
        self.phone = phone
        with SessionState._repo_lock:

             # ── Rescatamos (o creamos) el socio asociado ──
            self.socio:SocioBE = self._repo.get_by_phone(phone)
            if self.socio is None:
                self.socio = SocioBE(phone=phone)
                self._repo.persist(self.socio)

    

    def persist_socio(self) -> None:
        self._repo.persist(self.socio)
      

    def has_socio(self,phone:str) -> SocioBE | None:
        return self._repo.get_by_phone(phone)
    

