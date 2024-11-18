from datetime import datetime, timedelta
from schemas.cita import CitaCreate, CitaResponse
from core.config import citas_collection
from bson import ObjectId

def create_cita(cita: CitaCreate) -> CitaResponse:
    """Crea una nueva cita en la base de datos."""
    # Verifica que el horario de la cita sea válido
    fecha = cita.fecha_hora.date()
    hora_inicio = datetime.combine(fecha, datetime.strptime("07:00", "%H:%M").time())
    hora_fin = datetime.combine(fecha, datetime.strptime("19:00", "%H:%M").time())
    intervalo = timedelta(minutes=20)
    
    horario_valido = False
    horario_actual = hora_inicio
    while horario_actual <= hora_fin:
        if cita.fecha_hora == horario_actual:
            horario_valido = True
            break
        horario_actual += intervalo
    
    if not horario_valido:
        raise Exception("El horario de la cita no es válido. Debe ser entre 7 am y 7 pm con intervalos de 20 minutos.")
    
    # Verifica que el horario de la cita esté disponible
    cita_existente = citas_collection.find_one({"fecha_hora": cita.fecha_hora})
    if cita_existente:
        raise Exception("El horario de la cita ya está ocupado.")
    
    # Crea la cita
    cita_dict = cita.dict()
    cita_dict["estado"] = "confirmada"
    result = citas_collection.insert_one(cita_dict)
    cita_dict["id"] = str(result.inserted_id)
    return CitaResponse(**cita_dict)

def get_disponibilidad(fecha: datetime):
    """Obtiene la disponibilidad de horarios en una fecha específica."""
    # Genera todos los horarios posibles en el rango de 7 am a 7 pm con intervalos de 20 minutos
    horarios_disponibles = []
    hora_inicio = fecha.replace(hour=7, minute=0, second=0, microsecond=0)
    hora_fin = fecha.replace(hour=19, minute=0, second=0, microsecond=0)
    while hora_inicio <= hora_fin:
        horarios_disponibles.append(hora_inicio)
        hora_inicio += timedelta(minutes=20)

    # Obtiene las citas agendadas para la fecha específica
    fecha_inicio = fecha.replace(hour=0, minute=0, second=0, microsecond=0)
    fecha_fin = fecha.replace(hour=23, minute=59, second=59, microsecond=999999)
    registros = citas_collection.find({"fecha_hora": {"$gte": fecha_inicio, "$lte": fecha_fin}})

    # Marca los horarios que ya están agendados
    horarios_agendados = {registro["fecha_hora"] for registro in registros}
    disponibilidad = [horario for horario in horarios_disponibles if horario not in horarios_agendados]
    return disponibilidad

def get_cita_by_id(id_cita: str) -> CitaResponse:
    """Obtiene una cita específica por su ID."""
    cita = citas_collection.find_one({"_id": ObjectId(id_cita)})
    if cita:
        cita["id"] = str(cita["_id"])
        return CitaResponse(**cita)
    else:
        raise Exception("Cita no encontrada")

def get_citas_by_contacto(correo: str, fecha_inicio: datetime) -> list[CitaResponse]:
    """Obtiene todas las citas de un contacto desde una fecha específica hacia adelante."""
    citas = []
    query = {
        "correo": correo,
        "fecha_hora": {"$gte": fecha_inicio}
    }
    for cita in citas_collection.find(query):
        cita["id"] = str(cita["_id"])
        citas.append(CitaResponse(**cita))
    return citas