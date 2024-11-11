import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from schemas.cita import CitaCreate, CitaResponse
from core.config import GOOGLE_CREDENTIALS_FILE, SPREADSHEET_NAME

# Configuración de acceso a Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

def obtener_hoja_del_dia(fecha):
    fecha_str = fecha.strftime('%Y-%m-%d')
    sheet = client.open(SPREADSHEET_NAME)
    try:
        hoja = sheet.worksheet(fecha_str)
    except gspread.exceptions.WorksheetNotFound:
        hoja = sheet.add_worksheet(title=fecha_str, rows="100", cols="10")
        hoja.append_row(['id_cita', 'nombre_mascota', 'nombre_dueño', 'contacto', 'fecha_hora', 'medico', 'estado'])
        
        hora_inicio = datetime.combine(fecha, datetime.strptime("07:00", "%H:%M").time())
        hora_fin = datetime.combine(fecha, datetime.strptime("19:00", "%H:%M").time())
        intervalo = timedelta(minutes=20)
        
        horario_actual = hora_inicio
        id_cita = 1
        
        while horario_actual <= hora_fin:
            hoja.append_row([
                str(id_cita),
                '', '', '', 
                horario_actual.strftime('%Y-%m-%d %H:%M:%S'),
                '', 'disponible'
            ])
            horario_actual += intervalo
            id_cita += 1
            
    return hoja

def agendar_cita(cita: CitaCreate):
    fecha = cita.fecha_hora.date()
    hoja = obtener_hoja_del_dia(fecha)
    registros = hoja.get_all_records()
    
    for idx, registro in enumerate(registros, start=2):
        if registro['fecha_hora'] == cita.fecha_hora.strftime('%Y-%m-%d %H:%M:%S') and registro['estado'] == 'disponible':
            hoja.update(f'B{idx}:G{idx}', [
                [
                    cita.nombre_mascota,
                    cita.nombre_dueño,
                    cita.contacto,
                    cita.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
                    cita.medico,
                    'confirmada'
                ]
            ])
            return CitaResponse(
                id_cita=registro['id_cita'],
                nombre_mascota=cita.nombre_mascota,
                nombre_dueño=cita.nombre_dueño,
                contacto=cita.contacto,
                fecha_hora=cita.fecha_hora,
                medico=cita.medico,
                estado='confirmada'
            )
    raise Exception("El horario solicitado no está disponible")

def obtener_disponibilidad(fecha):
    hoja = obtener_hoja_del_dia(fecha)
    registros = hoja.get_all_records()
    disponibilidad = [
        {
            'fecha_hora': registro['fecha_hora'],
            'medico': registro['medico']
        } 
        for registro in registros if registro['estado'] == 'disponible'
    ]
    return disponibilidad
