import logging.config
import os
from pathlib import Path

# 1. Configuración de Directorios
# Crea un directorio 'logs' si no existe
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Rutas de los archivos de log
APP_LOG_FILE = LOGS_DIR / "app_operations.log"
AUDIT_LOG_FILE = LOGS_DIR / "magic_audit.log"
ERROR_LOG_FILE = LOGS_DIR / "error.log"


def configure_logging():
    """
    Configura el sistema de logging utilizando un diccionario de configuración.
    Define logs separados para la aplicación, la auditoría y los errores críticos.
    """
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,

        # 2. Formatters (Definición de formatos de salida)
        'formatters': {
            'standard': {
                # Formato estándar para logs de aplicación:
                # [Nivel] [Hora] [Nombre del Logger] - Mensaje
                'format': '%(levelname)s [%(asctime)s] %(name)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'audit_json': {
                # Formato estructurado para auditoría (simulando JSON para facilitar el análisis)
                'format': 'AUDIT_LOG - {"time": "%(asctime)s", "level": "%(levelname)s", "user": "%(user)s", "action": "%(action)s", "details": "%(message)s"}',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },

        # 3. Filters (Filtros personalizados)
        # Se requiere un filtro para inyectar datos de usuario/acción en el formato 'audit_json'
        # aunque la inyección real de 'user' y 'action' se hará vía el decorador AOP.

        # 4. Handlers (Destinos de los logs)
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',  # Salida a consola
                'stream': 'ext://sys.stdout',
            },
            'file_handler': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': APP_LOG_FILE,
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 5,
            },
            'audit_handler': {
                'level': 'INFO',
                'formatter': 'audit_json',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': AUDIT_LOG_FILE,
                'maxBytes': 1024 * 1024 * 10,  # 10 MB para auditoría
                'backupCount': 2,
            },
            'error_handler': {
                'level': 'ERROR',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': ERROR_LOG_FILE,
                'maxBytes': 1024 * 1024 * 1,
                'backupCount': 1,
            }
        },

        # 5. Loggers (Puntos de uso de los logs)
        'loggers': {
            '': {  # Logger raíz (Captura todos los mensajes no manejados)
                'handlers': ['default', 'file_handler', 'error_handler'],
                'level': 'INFO',
                'propagate': True
            },
            'magic_audit': {  # Logger específico para eventos de auditoría
                'handlers': ['audit_handler'],
                'level': 'INFO',
                'propagate': False  # NO propagar al logger raíz para mantener el archivo limpio
            },
            'uvicorn': {  # Logger del servidor
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': False
            },
        }
    }

    logging.config.dictConfig(LOGGING_CONFIG)


# Llamar a la configuración
configure_logging()

# Exportar loggers clave para su uso posterior
app_logger = logging.getLogger('root')
audit_logger = logging.getLogger('magic_audit')