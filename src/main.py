"""
Aplicación principal de FastAPI
Punto de entrada único de la aplicación
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import get_api_router
from src.core.config import PORT, HOST

# Crear instancia de FastAPI
app = FastAPI(
    title="Bran API",
    description="API para el servicio Bran",
    version="1.0.0",
    docs_url=None,  # Eliminado: /docs
    redoc_url=None,  # Eliminado: /redoc
    openapi_url=None  # Eliminado: /openapi.json
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todos los routers desde el centralizador
app.include_router(get_api_router())


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )
