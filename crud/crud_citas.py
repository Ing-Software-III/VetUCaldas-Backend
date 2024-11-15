from datetime import datetime, timedelta
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
            hoja.update(f'B{idx}:I{idx}', [
                [
                    cita.nombre_mascota,
                    cita.nombre_dueño,
                    cita.correo,
                    cita.telefono,
                    cita.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
                    cita.medico,
                    "confirmada",
                    cita.cedula
                ]
            ])
            return CitaResponse(
                id_cita=registro["id_cita"],
                nombre_mascota=cita.nombre_mascota,
                nombre_dueño=cita.nombre_dueño,
                correo=cita.correo,
                telefono=cita.telefono,
                fecha_hora=cita.fecha_hora,
                medico=cita.medico,
                estado="confirmada",
                cedula=cita.cedula
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
                correo=registro["correo"],
                telefono=registro["telefono"],
                fecha_hora=datetime.strptime(registro["fecha_hora"], '%Y-%m-%d %H:%M:%S'),
                medico=registro["medico"],
                estado=registro["estado"],
                cedula=registro["cedula"]
            )
    return None
def get_citas_by_contacto(correo: str, fecha_inicio: datetime) -> list[CitaResponse]:
    """Obtiene todas las citas de un contacto desde una fecha específica hacia adelante."""
    citas = []
    fecha_actual = fecha_inicio

    while True:
        hoja = obtener_hoja_del_dia(fecha_actual)
        registros = hoja.get_all_records()
        print(f"Procesando registros para la fecha: {fecha_actual}")

        for registro in registros:
            print(f"Registro: {registro}")
            fecha_hora = datetime.strptime(registro["fecha_hora"], '%Y-%m-%d %H:%M:%S')
            if "correo" in registro and registro["correo"] == correo and fecha_hora >= fecha_inicio:
                citas.append(CitaResponse(
                    id_cita=int(registro["id_cita"]),
                    nombre_mascota=registro["nombre_mascota"],
                    nombre_dueño=registro["nombre_dueño"],
                    correo=registro["correo"],
                    telefono=str(registro["telefono"]),
                    fecha_hora=fecha_hora,
                    medico=registro["medico"],
                    estado=registro["estado"],
                    cedula=str(registro["cedula"])
                ))

        # Avanza al siguiente día
        fecha_actual += timedelta(days=1)
        if fecha_actual > datetime.now() + timedelta(days=30):  # Limita la búsqueda a un año
            break

    return citas