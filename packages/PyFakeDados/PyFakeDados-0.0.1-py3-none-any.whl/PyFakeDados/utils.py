import random
from datetime import date, datetime, timedelta
from unidecode import unidecode

def remover_acentos(texto):
    texto_sem_acentos = unidecode(texto)
    return texto_sem_acentos

def gerar_data(data_inicial=None, data_final=None):

    # Definir um intervalo de datas para gerar datas aleatórias
    if data_inicial is None:
        data_inicial = datetime(1970, 1, 1)
    if data_final is None:
        data_final = datetime.now() - timedelta(days=30)
    
    # Gerar uma data aleatória dentro do intervalo definido
    diferenca = data_final - data_inicial
    dias_aleatorios = random.randint(0, diferenca.days)
    data_aleatoria = data_inicial + timedelta(days=dias_aleatorios)
    
    return data_aleatoria

def calcular_idade(data_nascimento):
    
    hoje = date.today()
    ano_atual = hoje.year
    mes_atual = hoje.month
    dia_atual = hoje.day

    ano_nascimento = data_nascimento.year
    mes_nascimento = data_nascimento.month
    dia_nascimento = data_nascimento.day

    idade = ano_atual - ano_nascimento

    if mes_atual < mes_nascimento or (mes_atual == mes_nascimento and dia_atual < dia_nascimento):
        idade -= 1

    return idade

def calcular_data_nascimento(idade):

    hoje = date.today()
    ano_atual = hoje.year

    ano_nascimento = ano_atual - idade
    data_nascimento = date(ano_nascimento, hoje.month, hoje.day)

    return data_nascimento

def gerar_data_nascimento(idade):
    
    hoje = date.today()
    ano_atual = hoje.year

    ano_nascimento = ano_atual - idade
    mes_nascimento = random.randint(1, 12)
    
    # Considerando meses com 30 dias
    if mes_nascimento == 2:
        dia_nascimento = random.randint(1, 28)
    elif mes_nascimento in [4, 6, 9, 11]:
        dia_nascimento = random.randint(1, 30)
    else:
        dia_nascimento = random.randint(1, 31)

    if mes_nascimento > hoje.month or (mes_nascimento == hoje.month and dia_nascimento >= hoje.day):
        ano_nascimento -= 1

    data_nascimento = date(ano_nascimento, mes_nascimento, dia_nascimento)

    return data_nascimento
