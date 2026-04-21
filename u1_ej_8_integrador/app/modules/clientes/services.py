from typing import List, Optional
from datetime import datetime
from . import schemas, models
from sqlmodel import Session, select

def crear(db: Session, data: schemas.ClienteCreate) -> models.ClienteModel:
    # Regla de negocio + validación
    existing = db.exec(select(models.ClienteModel).where(models.ClienteModel.email == data.email)).first()
    if existing:
        raise ValueError("El email ya está registrado en el sistema.")
    
    cliente_db = models.ClienteModel(**data.model_dump())
    db.add(cliente_db)
    db.commit()
    db.refresh(cliente_db)
    return cliente_db

def obtener_todas(
    skip: int = 0, 
    limit: int = 10, 
    nombre: Optional[str] = None, 
    activo: Optional[bool] = None
) -> List[schemas.ClienteRead]:
    resultados = list(_db.values())
    
    # Filtro avanzado por nombre (case-insensitive parcial)
    if nombre:
        resultados = [c for c in resultados if nombre.lower() in c.nombre.lower()]
    
    # Filtro por estado
    if activo is not None:
        resultados = [c for c in resultados if c.activo == activo]
        
    return resultados[skip:skip + limit]

def obtener_por_id(id: int) -> Optional[schemas.ClienteRead]:
    return _db.get(id)

def actualizar(id: int, data: schemas.ClienteUpdate) -> Optional[schemas.ClienteRead]:
    cliente = _db.get(id)
    if not cliente:
        return None
        
    #Regla de negocio: No actualizar si está desactivado
    if not cliente.activo:
        raise ValueError("No se pueden modificar clientes desactivados.")
        
    # Validación de email único
    if data.email and data.email != cliente.email and _buscar_por_email(data.email, excluir_id=id):
        raise ValueError("El nuevo email ya está en uso por otro cliente.")
        
    update_data = data.model_dump(exclude_unset=True)
    cliente_actualizado = cliente.model_copy(update=update_data)
    _db[id] = cliente_actualizado
    return cliente_actualizado

def desactivar(id: int) -> Optional[schemas.ClienteRead]:
    cliente = _db.get(id)
    if not cliente:
        return None
    cliente.activo = False
    _db[id] = cliente
    return cliente