from fastapi import APIRouter, HTTPException
from datetime import datetime
from schemas.cita import CitaCreate, CitaResponse
from crud.crud_citas import create_cita, get_disponibilidad

router = APIRouter()

@router.post("/agendar", response_model=CitaResponse)
async def crear_cita(cita: CitaCreate):
    try:
        cita_agendada = create_cita(cita)
        return cita_agendada
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/disponibilidad/{fecha}")
async def obtener_horarios_disponibles(fecha: str):
    try:
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
        disponibilidad = get_disponibilidad(fecha_dt)
        return disponibilidad
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD.")

