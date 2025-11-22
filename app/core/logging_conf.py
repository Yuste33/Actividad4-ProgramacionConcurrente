import logging.config
import os

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def setup_logging():
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            # Formato detallado para el archivo de auditoría (más campos)
            'auditor_format': {
                'format': '[%(asctime)s] | %(levelname)s | [%(name)s:%(lineno)d] | AuditorID: %(magic_id)s | Mensaje: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            # Formato simple para la consola
            'standard_format': {
                'format': '[%(levelname)s] [%(name)s] %(message)s',
            },
        },
        'handlers': {
            # Handler para la consola (para desarrolladores/debug)
            'console': {
                'level': 'INFO',
                'formatter': 'standard_format',
                'class': 'logging.StreamHandler',
            },
            # Handler para el archivo de Auditoría (logs de seguridad y negocio)
            'audit_file': {
                'level': 'INFO',
                'formatter': 'auditor_format',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'magical_audit.log'),
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 5,
            },
        },
        'loggers': {
            # Logger principal de la aplicación (para logs de negocio)
            'app_logger': {
                'handlers': ['console', 'audit_file'],
                'level': 'INFO',
                'propagate': False,
            },
            # Logger de FastAPI/Uvicorn
            'uvicorn': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        }
    }

    logging.config.dictConfig(logging_config)