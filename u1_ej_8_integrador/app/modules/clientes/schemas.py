from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre completo del cliente")
    email: EmailStr
    telefono: str = Field(..., pattern=r"^\+?[0-9]{7,15}$", description="Formato: +5491112345678 o 1112345678")

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, pattern=r"^\+?[0-9]{7,15}$")

class ClienteRead(ClienteBase):
    id: int
    fecha_registro: datetime
    activo: bool = True