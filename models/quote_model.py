from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


# Subdocumentos embebidos (estructuras internas)
class Printer(BaseModel):
    nombre: str
    watts: float
    tipo: str
    tecnologia: str
    velocidad: float
    nozzle: float
    capa: float
    temperatura: float

class Filament(BaseModel):
    nombre: str
    tipo: str
    diametro: float
    precio_kg: float
    color: str
    peso_total: float

class Energy(BaseModel):
    costo_kwh: float

class ModelData(BaseModel):
    peso_modelo: float
    tiempo_impresion: float
    infill: float
    soportes: bool
    tipo_soporte: Optional[str]
    peso_soportes: float
    altura_capa: float

class Commercial(BaseModel):
    costo_hora: float
    mano_obra: float
    postprocesado: float
    margen: float
    impuestos: float

class Summary(BaseModel):
    costo_total_estimado: float
    gramos_usados: float
    gramos_desechados: float
    porcentaje_desecho: float
    sugerencias: Optional[list[str]] = []


# Documento principal
class Quote(Document):
    user_id: ObjectId
    quote_name: str
    printer: Printer
    filament: Filament
    energy: Energy
    model: ModelData
    commercial: Commercial
    summary: Summary
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "quotes"

    class Config:
        arbitrary_types_allowed = True
    '''
    arbitrary_types_allowed = True 
    En este bloque ver una forma de no pasar los objects id ya que pydantic 
    ya no soporta el object id de mongoDB y toca pasarlo manualemnte y decirle
    que ese tipo de dato esta bien y controlado.
    '''