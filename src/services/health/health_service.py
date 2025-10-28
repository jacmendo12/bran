"""
Servicio para health check del servidor
"""
from datetime import datetime
import platform
import sys
from typing import Dict, Any


class HealthService:
    """
    Servicio que maneja la lógica de health check
    """
    
    @staticmethod
    def get_health_status() -> Dict[str, Any]:
        """
        Obtiene el estado completo del servidor
        
        Returns:
            Dict con información del estado del servidor
        """
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "bran-api",
            "version": "1.0.0",
            "python_version": sys.version.split()[0],
            "platform": platform.system(),
            "architecture": platform.machine()
        }
    
    @staticmethod
    def get_liveness() -> Dict[str, Any]:
        """
        Verifica si el servicio está vivo
        
        Returns:
            Dict con estado de liveness
        """
        return {
            "alive": True,
            "timestamp": datetime.utcnow().isoformat()
        }
