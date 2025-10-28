"""
Configuración central de la aplicación
"""
import os
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path(__file__).parent.parent.parent
SRC_DIR = BASE_DIR / "src"
UPLOADS_DIR = BASE_DIR / "uploads"
IMAGES_DIR = SRC_DIR / "imagenes"

# Configuración de la API
PORT = int(os.getenv("PORT", 3000))
HOST = os.getenv("HOST", "0.0.0.0")

# Configuración de Telegram Bot
# TELEGRAM_BOT_TOKEN = "836265911:AAHEzhFeHeUnQfkSfHc_K2ucmW7GGbFndvw"  # Test
TELEGRAM_BOT_TOKEN = "7979473682:AAGrztiOP_LTt7O2K_gw-Y93wvGryX8XCgo"  # Kairen

# Configuración del scheduler
SCHEDULER_INTERVAL_HOURS = 1
SCHEDULER_INTERVAL_MINUTES = 15

# Configuración de logging
LOGGING_LEVEL = "INFO"

# Configuración de hilos
MAX_WORKERS = 3
