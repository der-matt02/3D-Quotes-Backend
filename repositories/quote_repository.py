from typing import List, Optional
from models.quote_model import Quote
from schemas.quote_schemas import QuoteCreateSchema, QuoteUpdateSchema
from bson import ObjectId


# Crear nueva cotización
async def create_quote(user_id: ObjectId, data: QuoteCreateSchema) -> Quote:
    quote = Quote(
        user_id=user_id,
        quote_name=data.quote_name,
        printer=data.printer,
        filament=data.filament,
        energy=data.energy,
        model=data.model,
        commercial=data.commercial,
        summary=await calculate_summary(data)  # Placeholder
    )
    return await quote.insert()


# Obtener cotización por ID NOTA: para mostrar o validar propiedad
async def get_quote_by_id(quote_id: str) -> Optional[Quote]:
    return await Quote.get(ObjectId(quote_id))


# Obtener todas las cotizaciones de un usuario
async def get_quotes_by_user(user_id: ObjectId) -> List[Quote]:
    return await Quote.find(Quote.user_id == user_id).to_list()


# Actualizar una cotización
async def update_quote(quote_id: str, data: QuoteUpdateSchema) -> Optional[Quote]:
    quote = await Quote.get(ObjectId(quote_id))
    if not quote:
        return None

    update_data = data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(quote, field, value)

    quote.updated_at = quote.updated_at.utcnow()
    return await quote.save()


# Eliminar cotización
async def delete_quote(quote_id: str) -> bool:
    quote = await Quote.get(ObjectId(quote_id))
    if not quote:
        return False
    await quote.delete()
    return True


# Placeholder para cálculo de resumen (lo definimos después)
async def calculate_summary(data: QuoteCreateSchema):
    return {
        "costo_total_estimado": 0,
        "gramos_usados": 0,
        "gramos_desechados": 0,
        "porcentaje_desecho": 0,
        "sugerencias": []
    }
