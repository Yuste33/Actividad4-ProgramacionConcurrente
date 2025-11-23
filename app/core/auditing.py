import logging
from functools import wraps

logger = logging.getLogger("app_logger")


# Este decorador intercepta la ejecucion de una funcion para registrarla
def audit_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Iniciando operacion {func.__name__}", extra={"magic_id": "SYSTEM"})

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {str(e)}", extra={"magic_id": "SYSTEM"})

        logger.info(f"Finalizando operacion {func.__name__}", extra={"magic_id": "SYSTEM"})

        return result

    return wrapper
