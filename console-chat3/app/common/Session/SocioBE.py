# 2.  Modelo de dominio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional,Self


@dataclass
class SocioBE:
    phone: str
    nro_socio: Optional[str] = None
    nro_abonado: Optional[str] = None
    nombre: Optional[str] = None
    alta: datetime = datetime.now()
    @classmethod
    def from_dict(cls, phone: str, data: Dict[str, Any]) -> "SocioBE":
        return cls(
            phone=phone,
            nro_socio=data.get("nro_socio"),
            nro_abonado=data.get("nro_abonado"),
            nombre=data.get("nombre"),
            alta=datetime.fromisoformat(data.get("alta")) if data.get("alta") else datetime.now()
        )