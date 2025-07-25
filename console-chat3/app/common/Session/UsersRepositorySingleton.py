from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List

from app.common.Session.SocioBE import SocioBE
from app.common.app_constants import AppConstants
from langchain.schema import BaseMessage  # necesitás la import que ya usás

# ──────────────────────────────────────────────────────────────────────────────
# Config global
DATA_DIR   = Path(AppConstants.API_LOGS_PATH.value) / "data"
USERS_FILE = DATA_DIR / "users.json"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ──────────────────────────────────────────────────────────────────────────────
# Repositorio de usuarios
class UsersRepositorySingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UsersRepositorySingleton, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
   
    def __init__(self):
        if self._initialized:
            return
        self._data: Dict[str, SocioBE] = {}
        self._lock = Lock()
        self._load()
        self._initialized = True
   
    def _load(self) -> None:
        # if self._data is None:            # ⇢ primera vez
            if USERS_FILE.exists():
                    with USERS_FILE.open("r", encoding="utf-8") as f:
                        raw: Dict[str, Dict[str, Any]] = json.load(f)
                   
                    for phone, rec in raw.items():
                        self._data[phone] = SocioBE.from_dict(phone, rec)
            else:
                self._data = {}

  

    def get_by_phone(self, phone: str) -> "SocioBE" | None:
        """Obtiene el socio asociado al teléfono."""
        socio = self._data.get(phone) 
        return socio
    
  
    def persist( self,socio: SocioBE) -> None:
        """Agrega o actualiza un socio."""
        self._data[socio.phone] = socio
        self.save()
        


    def save(self) -> None:
        with self._lock:
            with USERS_FILE.open("w", encoding="utf-8") as f:
                json.dump(
                    {phone: asdict(socio) for phone, socio in self._data.items()},
                    f,
                    ensure_ascii=False,
                    indent=2,
                    default=str  # para datetime
                )

    # @classmethod
    # def save(self) -> None:
    #     """Graba el estado actual en disco (atómico)."""
    #     # self._ensure_loaded()
    #     with self._lock:  # evita escrituras simultáneas
    #         with USERS_FILE.open("w", encoding="utf-8") as f:
    #             json.dump(self._data, f, ensure_ascii=False, indent=2)

