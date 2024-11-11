from datetime import datetime
from schemas.cita import CitaCreate, CitaResponse
from services.google_sheets import obtener_hoja_del_dia

def create_cita(cita: CitaCreate) -> CitaResponse:
    """Crea o actualiza una cita en la hoja del día, en el horario especificado."""
    fecha = cita.fecha_hora.date()
    hoja = obtener_hoja_del_dia(fecha)
    
    registros = hoja.get_all_records()
    
    # Busca el horario específico y verifica que esté disponible
    for idx, registro in enumerate(registros, start=2):  # start=2 para ajustar el índice de fila en Google Sheets
        if registro["fecha_hora"] == cita.fecha_hora.strftime('%Y-%m-%d %H:%M:%S') and registro["estado"] == "disponible":
            # Actualiza la fila correspondiente con los datos de la cita
            hoja.update(f'B{idx}:G{idx}', [
                [
                    cita.nombre_mascota,
                    cita.nombre_dueño,
                    cita.contacto,
                    cita.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
                    cita.medico,
                    "confirmada"
                ]
            ])
            return CitaResponse(
                id_cita=registro["id_cita"],
                nombre_mascota=cita.nombre_mascota,
                nombre_dueño=cita.nombre_dueño,
                contacto=cita.contacto,
                fecha_hora=cita.fecha_hora,
                medico=cita.medico,
                estado="confirmada"
            )
    
    # Si no encuentra el horario disponible, lanza una excepción
    raise Exception("El horario solicitado no está disponible")

def get_disponibilidad(fecha: datetime):
    """Obtiene la disponibilidad de horarios en una fecha específica."""
    hoja = obtener_hoja_del_dia(fecha)
    registros = hoja.get_all_records()
    disponibilidad = [
        {
            "fecha_hora": registro["fecha_hora"],
            "medico": registro["medico"]
        }
        for registro in registros if registro["estado"] == "disponible"
    ]
    return disponibilidad

def get_cita_by_id(fecha: datetime, id_cita: str) -> CitaResponse:
    """Obtiene una cita específica por su ID en una fecha dada."""
    hoja = obtener_hoja_del_dia(fecha)
    registros = hoja.get_all_records()
    
    for registro in registros:
        if registro["id_cita"] == id_cita:
            return CitaResponse(
                id_cita=id_cita,
                nombre_mascota=registro["nombre_mascota"],
                nombre_dueño=registro["nombre_dueño"],
                contacto=registro["contacto"],
                fecha_hora=datetime.strptime(registro["fecha_hora"], '%Y-%m-%d %H:%M:%S'),
                medico=registro["medico"],
                estado=registro["estado"]
            )
    return None
