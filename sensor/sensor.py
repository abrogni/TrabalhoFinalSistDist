import requests
import time
import random
import sys

COLETOR_URL = "http://coletor:5000/leitura"

def gerar_dado():
    return {
        "sensor_id": random.randint(1, 100),
        "temperatura": round(random.uniform(20, 40), 2),
        "umidade": round(random.uniform(40, 80), 2)
    }

while True:
    time.sleep(random.uniform(1, 3))

    if random.random() < 0.1:
        print("Falha simulada no sensor!", file=sys.stderr)
        raise Exception("Sensor falhou")

    dado = gerar_dado()
    try:
        r = requests.post(COLETOR_URL, json=dado)
        print(f"→ Enviado: {dado} | Status: {r.status_code}")
    except Exception as e:
        print(f"Erro ao enviar dado: {e}", file=sys.stderr)
