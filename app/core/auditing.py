import logging
import time
from functools import wraps

logger = logging.getLogger("app_logger")


# Este decorador intercepta la ejecucion de una funcion para registrarla
def audit_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Iniciando operacion {func.__name__}", extra={"magic_id": "SYSTEM"})
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {str(e)}", extra={"magic_id": "SYSTEM"})

        logger.info(f"Finalizando operacion {func.__name__}", extra={"magic_id": "SYSTEM"})
        end_time = time.time()

        duration = end_time - start_time

        logger.info(f"Tiempo: {duration:.4f} segundos", extra={"magic_id": "SYSTEM"})
        return result

    return wrapper
