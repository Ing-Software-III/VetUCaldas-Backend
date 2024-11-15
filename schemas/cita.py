from pydantic import BaseModel, Field
from datetime import datetime

class CitaCreate(BaseModel):
    nombre_mascota: str = Field(..., example="Firulais")
    nombre_dueño: str = Field(..., example="Juan Pérez")
    correo: str = Field(..., example="juan.perez@gmail.com")
    telefono: str = Field(..., example="1234567890")
    fecha_hora: datetime = Field(..., example="2024-12-01T10:30:00")
    medico: str = Field(..., example="Dra. María López")
    cedula: str = Field(..., example="123456789")

class CitaResponse(BaseModel):
    id_cita: int
    nombre_mascota: str
    nombre_dueño: str
    correo: str
    telefono: str
    fecha_hora: datetime
    medico: str
    estado: str = Field(..., example="confirmada")
    cedula: str = Field(..., example="123456789")