from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PrinterSchema(BaseModel):
    nombre: str
    watts: float
    tipo: str
    tecnologia: str
    velocidad: float
    nozzle: float
    capa: float
    temperatura: float

class FilamentSchema(BaseModel):
    nombre: str
    tipo: str
    diametro: float
    precio_kg: float
    color: str
    peso_total: float

class EnergySchema(BaseModel):
    costo_kwh: float

class ModelDataSchema(BaseModel):
    peso_modelo: float
    tiempo_impresion: float
    infill: float
    soportes: bool
    tipo_soporte: Optional[str]
    peso_soportes: float
    altura_capa: float

class CommercialSchema(BaseModel):
    costo_hora: float
    mano_obra: float
    postprocesado: float
    margen: float
    impuestos: float

class SummarySchema(BaseModel):
    costo_total_estimado: float
    gramos_usados: float
    gramos_desechados: float
    porcentaje_desecho: float
    sugerencias: Optional[List[str]] = []


# Schema para crear cotizaciones
class QuoteCreateSchema(BaseModel):
    quote_name: str
    printer: PrinterSchema
    filament: FilamentSchema
    energy: EnergySchema
    model: ModelDataSchema
    commercial: CommercialSchema

# Schema para actualizar cotizaciones
class QuoteUpdateSchema(BaseModel):
    quote_name: Optional[str]
    printer: Optional[PrinterSchema]
    filament: Optional[FilamentSchema]
    energy: Optional[EnergySchema]
    model: Optional[ModelDataSchema]
    commercial: Optional[CommercialSchema]

# Schema para mostrar cotizaciones
class QuoteOutSchema(BaseModel):
    id: str
    user_id: str
    quote_name: str
    printer: PrinterSchema
    filament: FilamentSchema
    energy: EnergySchema
    model: ModelDataSchema
    commercial: CommercialSchema
    summary: SummarySchema
    created_at: datetime
    updated_at: datetime
