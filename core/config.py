import os

# Ruta al archivo de credenciales de Google
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOOGLE_CREDENTIALS_FILE = os.path.join(BASE_DIR, 'core', 'vetucaldas-api-33f60c7f349c.json')
SPREADSHEET_NAME = 'VetUCaldas_Citas'
