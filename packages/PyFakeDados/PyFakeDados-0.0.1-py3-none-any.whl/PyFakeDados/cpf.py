import random
import itertools

def validar_cpf(cpf):
    # Remove caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador e compara com o CPF fornecido
    soma = sum(int(x) * y for x, y in zip(cpf[:9], itertools.count(10, -1)))
    if (11 - (soma % 11)) % 11 != int(cpf[9]):
        return False

    # Calcula o segundo dígito verificador e compara com o CPF fornecido
    soma = sum(int(x) * y for x, y in zip(cpf[:10], itertools.count(11, -1)))
    if (11 - (soma % 11)) % 11 != int(cpf[10]):
        return False

    return True

def gerar_cpf(mask=False):
    # Gera os nove primeiros dígitos do CPF de forma aleatória
    cpf = [random.randint(0, 9) for _ in range(9)]

    # Calcula o primeiro dígito verificador
    soma = sum(x * y for x, y in zip(cpf, itertools.count(10, -1)))
    cpf.append((11 - (soma % 11)) % 11)

    # Calcula o segundo dígito verificador
    soma = sum(x * y for x, y in zip(cpf, itertools.count(11, -1)))
    cpf.append((11 - (soma % 11)) % 11)

    if mask:
        cpf = f"{cpf[0]}{cpf[1]}{cpf[2]}.{cpf[3]}{cpf[4]}{cpf[5]}.{cpf[6]}{cpf[7]}{cpf[8]}-{cpf[9]}{cpf[10]}"
    else:
        cpf = ''.join([str(num) for num in cpf])

    # Retorna o CPF formatado (XXX.XXX.XXX-XX)
    return cpf
