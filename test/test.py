import pytest
from fastapi.testclient import TestClient
from main import app  # Asegúrate de que 'app' es la instancia de FastAPI en tu aplicación

client = TestClient(app)

def test_crear_cita():
    response = client.post("/agendar", json={
        "nombre_mascota": "Firulais",
        "nombre_dueño": "Juan Pérez",
        "correo": "juan.perez@gmail.com",
        "telefono": "1234567890",
        "fecha_hora": "2024-12-01T10:30:00",
        "medico": "Dra. María López",
        "cedula": "123456789"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_mascota"] == "Firulais"
    assert data["nombre_dueño"] == "Juan Pérez"
    assert data["correo"] == "juan.perez@gmail.com"
    assert data["telefono"] == "1234567890"
    assert data["fecha_hora"] == "2024-12-01T10:30:00"
    assert data["medico"] == "Dra. María López"
    assert data["cedula"] == "123456789"

def test_obtener_horarios_disponibles():
    response = client.get("/disponibilidad/2024-12-01")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_obtener_citas_por_contacto():
    response = client.get("/citas/juan.perez@gmail.com?fecha_inicio=2024-12-01")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for cita in data:
        assert cita["correo"] == "juan.perez@gmail.com"
        assert datetime.strptime(cita["fecha_hora"], '%Y-%m-%dT%H:%M:%S') >= datetime.strptime("2024-12-01", '%Y-%m-%d')