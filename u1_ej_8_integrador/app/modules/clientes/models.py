from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class ClienteModel(SQLModel, table=True):
    __tablename__ = "clientes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, index=True)
    email: str = Field(unique=True, max_length=100, index=True)
    telefono: str = Field(max_length=15)
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)
    activo: bool = Field(default=True)