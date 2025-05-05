from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.quote_schemas import QuoteCreateSchema, QuoteUpdateSchema, QuoteOutSchema
from services import quote_service
from dependencies.auth import get_current_user
from models.user_model import User

router = APIRouter()

# Crear cotización
@router.post("", response_model=QuoteOutSchema, status_code=status.HTTP_201_CREATED)
async def create_quote(data: QuoteCreateSchema, current_user: User = Depends(get_current_user)):
    quote = await quote_service.create_quote_for_user(current_user.id, data)
    return quote


# Obtener todas mis cotizaciones
@router.get("", response_model=List[QuoteOutSchema])
async def list_quotes(current_user: User = Depends(get_current_user)):
    return await quote_service.get_user_quotes(current_user.id)


# Obtener cotización específica
@router.get("/{quote_id}", response_model=QuoteOutSchema)
async def get_quote(quote_id: str, current_user: User = Depends(get_current_user)):
    quote = await quote_service.get_quote_by_id(quote_id)
    if not quote or quote.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    return quote


# Editar cotización
@router.put("/{quote_id}", response_model=QuoteOutSchema)
async def update_quote(quote_id: str, data: QuoteUpdateSchema, current_user: User = Depends(get_current_user)):
    quote = await quote_service.get_quote_by_id(quote_id)
    if not quote or quote.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")

    updated = await quote_service.update_quote(quote_id, data)
    return updated


# Eliminar cotización
@router.delete("/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quote(quote_id: str, current_user: User = Depends(get_current_user)):
    quote = await quote_service.get_quote_by_id(quote_id)
    if not quote or quote.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")

    success = await quote_service.delete_quote(quote_id)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo eliminar la cotización")
    return
