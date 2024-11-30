from fastapi import FastAPI
from core.config import citas_collection
from api.endpoints import citas
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las solicitudes de origen cruzado
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test-db")
async def test_db():
    try:
        # Intenta insertar un documento de prueba
        result = citas_collection.insert_one({"test": "data"})
        # Elimina el documento de prueba
        citas_collection.delete_one({"_id": result.inserted_id})
        return {"message": "Connection to MongoDB Atlas is successful"}
    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}
    
    
app.include_router(citas.router, prefix="/citas")