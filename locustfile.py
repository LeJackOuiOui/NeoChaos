from locust import HttpUser, between, task
import random


class Cliente(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def solicitar_descuento_rapido(self):
        payload = {"usuario_id": str(random.randint(1000, 9999))}

        with self.client.post(
            "/aplicar-descuento", json=payload, catch_response=True
        ) as response:
            if response.status_code == 202:
                response.success()
            else:
                response.failure(f"Error inesperado: {response.status_code}")

    @task(1)
    def flujo_completo_polling(self):
        payload = {"usuario_id": "9999"}
        response = self.client.post("/aplicar-descuento", json=payload)
        if response.status_code == 202:
            datos = response.json()
            task_id = datos.get("task_id")
            if task_id:
                self.client.get(
                    f"/estado-descuento/{task_id}", name="/estado-descuento/[id]"
                )

    @task(1)
    def revisar_salud(self):
        self.client.get("/health")

    # @task(1)
    # def hacer_compra(self):
    #     self.client.post("/comprar")

    # @task(2)
    # def probar_error_aleatorio(self):
    #     with self.client.get("/error_aleatorio", catch_response=True) as response:
    #         if response.status_code == 500:
    #             response.failure("Ocurrio un error 500 simulado por la API")

    # @task(1)
    # def probar_fuga_ram(self):
    #     with self.client.get("/memoria_ram", catch_response=True) as response:
    #         if response.status_code == 502 or response.status_code == 504:
    #             response.failure("El contenedor murió o no respondió (OOM killed / Timeout)")

    # @task(1)
    # def revisar_version(self):
    #     self.client.get("/version")

    # @task(1)
    # def aplicar_descuento(self):
    #     self.client.post("/aplicar-descuento")
