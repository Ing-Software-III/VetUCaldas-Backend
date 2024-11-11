from services.google_sheets import client, SPREADSHEET_NAME

# Acceder al Google Sheets
sheet = client.open(SPREADSHEET_NAME)

# Obtener una lista de hojas (pestañas)
worksheets = sheet.worksheets()
print("Hojas disponibles:")
for ws in worksheets:
    print(ws.title)
