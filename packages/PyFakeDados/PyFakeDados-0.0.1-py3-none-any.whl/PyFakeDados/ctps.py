import random

def gerar_ctps():
    numero_ctps = random.randint(100000000000, 999999999999)
    numero_ctps_formatado = f"{numero_ctps:013}"
    return numero_ctps_formatado

