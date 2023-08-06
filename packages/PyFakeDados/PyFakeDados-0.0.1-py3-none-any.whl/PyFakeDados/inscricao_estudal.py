import random

def gerar_inscricao_estadual():
    numeros = ''.join(str(random.randint(0, 9)) for _ in range(8))
    inscricao = f'{numeros}'
    return inscricao
