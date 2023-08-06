import random

def gerar_pis():
    numero_pis = random.randint(10000000000, 99999999999)
    numero_pis_formatado = f"{numero_pis:011}"
    return numero_pis_formatado

