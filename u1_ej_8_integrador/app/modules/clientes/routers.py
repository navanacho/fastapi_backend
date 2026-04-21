from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List, Optional
from . import schemas, services

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=schemas.ClienteRead, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: schemas.ClienteCreate):
    try:
        return services.crear(cliente)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/", response_model=List[schemas.ClienteRead], status_code=status.HTTP_200_OK)
def listar_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    nombre: Optional[str] = Query(None, min_length=3, description="Filtrar por nombre (contiene)"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo")
):
    return services.obtener_todas(skip, limit, nombre, activo)

@router.get("/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def detalle_cliente(id: int = Path(..., gt=0)):
    cliente = services.obtener_por_id(id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente

@router.put("/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def actualizar_cliente(
    id: int = Path(..., gt=0),
    datos: str = schemas.ClienteUpdate
):
    try:
        actualizado = services.actualizar(id, datos)
        if not actualizado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
        return actualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id}/desactivar", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def desactivar_cliente(id: int = Path(..., gt=0)):
    desactivado = services.desactivar(id)
    if not desactivado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return desactivado