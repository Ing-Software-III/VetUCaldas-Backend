from pydantic import BaseModel, Field
from datetime import datetime

class CitaCreate(BaseModel):
    nombre_mascota: str = Field(..., example="Firulais")
    nombre_dueño: str = Field(..., example="Juan Pérez")
    contacto: str = Field(..., example="juan.perez@gmail.com")
    fecha_hora: datetime = Field(..., example="2024-12-01T10:30:00")
    medico: str = Field(..., example="Dra. María López")

class CitaResponse(BaseModel):
    id_cita: int
    nombre_mascota: str
    nombre_dueño: str
    contacto: str
    fecha_hora: datetime
    medico: str
    estado: str = Field(..., example="confirmada")
