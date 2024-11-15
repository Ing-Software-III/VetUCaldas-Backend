from fastapi import APIRouter, HTTPException
from datetime import datetime
from schemas.cita import CitaCreate, CitaResponse
from crud.crud_citas import create_cita, get_disponibilidad, get_citas_by_contacto

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

@router.get("/citas/{correo}", response_model=list[CitaResponse])
async def obtener_citas_por_contacto(correo: str, fecha_inicio: str):
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        citas = get_citas_by_contacto(correo, fecha_inicio_dt)
        print("fecha_inicio_dt", fecha_inicio_dt, "fecha string", fecha_inicio)
        return citas
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))