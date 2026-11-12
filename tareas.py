import random
import time
import os
from celery import Celery

broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app = Celery("tareas", broker=broker_url)


def llamar_pasarela_bancaria():
    time.sleep(random.uniform(1, 4))
    if random.random() < 0.3:
        raise Exception("Error 504: El banco no responde")
    return "Pago Aprobado"


@celery_app.task(bind=True, max_retries=3, soft_time_limit=5)
def procesar_descuento(self, usuario_id):
    try:
        resultado_banco = llamar_pasarela_bancaria()
        return f"Ticket comprado con éxito para el usuario {usuario_id}. Estado: {resultado_banco}"
    except Exception as exc:
        try:
            # Reintenta automáticamente esperando 2 segundos entre cada intento
            raise self.retry(exc=exc, countdown=2)
        except self.MaxRetriesExceededError:
            raise Exception("El banco rechazó la tarjeta tras 3 reintentos fallidos.")
