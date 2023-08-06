import random
from PyFakeDados.utils import remover_acentos

provedores = ['gmail.com', "yahoo.com", "hotmail.com", "outlook.com",]
dominios = ['com', "com.br", "xyz", "info",]

def gerar_email(nome):
    nome = remover_acentos(nome)
    nome = nome.lower().replace(" ", "")
    dominio = random.choice(dominios)
    email = f'{nome}@{nome}.{dominio}'
    return email

def gerar_email_empresa(nome):
    nome = remover_acentos(nome)
    nome = nome.lower().replace(" ", "")
    provedor = nome
    dominio = random.choice(dominios)
    email = f'contato@{nome}.{dominio}'
    return email

def gerar_email_pessoa(nome):
    nome = remover_acentos(nome)
    nome = nome.lower().replace(" ", "")
    provedor = random.choice(provedores)
    email = f'{nome}@{provedor}'
    return email