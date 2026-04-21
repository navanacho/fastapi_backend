from fastapi import Depends
from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List, Optional
from . import schemas, services
from sqlmodel import Session
from app.dataBase import get_session

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=schemas.ClienteRead, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_session)):
    try:
        return services.crear(db, cliente)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/", response_model=List[schemas.ClienteRead])
def listar_clientes(
    skip: int = Query(0, ge=0), limit: int = Query(10, le=50),
    nombre: Optional[str] = Query(None, min_length=3),
    activo: Optional[bool] = Query(None),
    db: Session = Depends(get_session)
):
    return services.obtener_todas(db, skip, limit, nombre, activo)


router.get("/{id}", response_model=schemas.ClienteRead)
def detalle_cliente(id: int = Path(..., gt=0), db: Session = Depends(get_session)):
    cliente = services.obtener_por_id(db, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.put("/{id}", response_model=schemas.ClienteRead)
def actualizar_cliente(
    id: int = Path(..., gt=0), datos: schemas.ClienteUpdate = ...,
    db: Session = Depends(get_session)
):
    try:
        actualizado = services.actualizar(db, id, datos)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return actualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id}/desactivar", response_model=schemas.ClienteRead)
def desactivar_cliente(id: int = Path(..., gt=0), db: Session = Depends(get_session)):
    desactivado = services.desactivar(db, id)
    if not desactivado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return desactivado