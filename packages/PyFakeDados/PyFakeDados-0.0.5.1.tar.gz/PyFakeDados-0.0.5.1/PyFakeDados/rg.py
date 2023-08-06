import random

def gerar_rg(mask=False):

    numero_rg = ""

    # Geração dos números principais do RG
    for _ in range(8):
        numero_rg += str(random.randint(0, 9))

    # Geração do dígito verificador do RG
    soma = 0
    for i in range(8):
        soma += int(numero_rg[i]) * (9 - i)

    digito_verificador = soma % 11
    if digito_verificador == 10:
        digito_verificador = "X"
    else:
        digito_verificador = str(digito_verificador)

    numero_rg += digito_verificador

    if mask:
        numero_rg = f"{numero_rg[:2]}.{numero_rg[2:5]}.{numero_rg[5:8]}-{numero_rg[8]}"

    return numero_rg
