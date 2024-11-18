from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class CitaCreate(BaseModel):
    nombre_mascota: str = Field(..., example="Firulais")
    nombre_dueño: str = Field(..., example="Juan Pérez")
    correo: str = Field(..., example="juan.perez@gmail.com")
    telefono: str = Field(..., example="1234567890")
    fecha_hora: datetime = Field(..., example="2024-12-01T10:30:00")
    medico: str = Field(..., example="Dra. María López")
    cedula: str = Field(..., example="123456789")

class CitaResponse(BaseModel):
    id: str
    nombre_mascota: str
    nombre_dueño: str
    correo: str
    telefono: str
    fecha_hora: datetime
    medico: str
    estado: str
    cedula: str

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: str
        }