import random
import itertools

def gerar_cnpj(mask=False):
    
    while True:

        # Gera os oito primeiros dígitos do CNPJ de forma aleatória
        cnpj = [random.randint(0, 9) for _ in range(8)]

        # Gera os quatro dígitos de controle
        cnpj += [0, 0, 0, 1]

        # Calcula o primeiro dígito verificador
        soma = sum(x * y for x, y in zip(cnpj, itertools.cycle(range(2, 10))))
        cnpj.append((11 - (soma % 11)) % 11)

        # Calcula o segundo dígito verificador
        soma = sum(x * y for x, y in zip(cnpj, itertools.cycle(range(2, 10)))) + 2 * cnpj[8]
        cnpj.append((11 - (soma % 11)) % 11)

        # Verifica se o CNPJ gerado é válido
        if validar_cnpj(''.join(map(str, cnpj))):
            break
    
    if mask:
        cnpj = f"{cnpj[0]}{cnpj[1]}.{cnpj[2]}{cnpj[3]}{cnpj[4]}.{cnpj[5]}{cnpj[6]}{cnpj[7]}/{cnpj[8]}{cnpj[9]}{cnpj[10]}{cnpj[11]}-{cnpj[12]}{cnpj[13]}"
    else:
        cnpj = ''.join([str(num) for num in cnpj])

    # Retorna o CNPJ formatado (XX.XXX.XXX/XXXX-XX)
    return cnpj

def validar_cnpj(cnpj):
    # Remove caracteres não numéricos do CNPJ
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Verifica se o CNPJ possui 14 dígitos
    if len(cnpj) != 14:
        return False

    # Calcula o primeiro dígito verificador e compara com o CNPJ fornecido
    soma = sum(int(x) * y for x, y in zip(cnpj[:12], itertools.cycle(range(2, 10))))
    if (11 - (soma % 11)) % 11 != int(cnpj[12]):
        return False

    # Calcula o segundo dígito verificador e compara com o CNPJ fornecido
    soma = sum(int(x) * y for x, y in zip(cnpj[:13], itertools.cycle(range(2, 10)))) + 2 * int(cnpj[12])
    if (11 - (soma % 11)) % 11 != int(cnpj[13]):
        return False

    return True
