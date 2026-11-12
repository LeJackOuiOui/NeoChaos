import time
import os
from celery import Celery

broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app = Celery("tareas", broker=broker_url)


@celery_app.task
def procesar_descuento(usuario_id):
    time.sleep(1.2)
    return f"Descuento del 15% valido y aplicado para {usuario_id}"
