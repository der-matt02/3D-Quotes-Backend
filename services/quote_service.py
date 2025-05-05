from typing import List, Optional
from schemas.quote_schemas import QuoteCreateSchema, QuoteUpdateSchema, QuoteOutSchema
from models.quote_model import Quote
from repositories import quote_repository
from bson import ObjectId


# Crear cotización con cálculo de resumen
async def create_quote_for_user(user_id: ObjectId, data: QuoteCreateSchema) -> Quote:
    # Cálculo de resumen (puede ir mejorando luego)
    summary = await quote_repository.calculate_summary(data)

    quote = Quote(
        user_id=user_id,
        quote_name=data.quote_name,
        printer=data.printer,
        filament=data.filament,
        energy=data.energy,
        model=data.model,
        commercial=data.commercial,
        summary=summary
    )
    return await quote.insert()


# Obtener cotización por ID (usada en GET o validación de propietario)
async def get_quote_by_id(quote_id: str) -> Optional[Quote]:
    return await quote_repository.get_quote_by_id(quote_id)


# Obtener todas las cotizaciones del usuario actual
async def get_user_quotes(user_id: ObjectId) -> List[Quote]:
    return await quote_repository.get_quotes_by_user(user_id)


# Editar una cotización
async def update_quote(quote_id: str, data: QuoteUpdateSchema) -> Optional[Quote]:
    return await quote_repository.update_quote(quote_id, data)


# Eliminar una cotización
async def delete_quote(quote_id: str) -> bool:
    return await quote_repository.delete_quote(quote_id)
