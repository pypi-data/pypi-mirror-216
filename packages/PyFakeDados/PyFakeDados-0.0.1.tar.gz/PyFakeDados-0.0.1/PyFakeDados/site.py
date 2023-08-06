import random
from PyFakeDados.utils import remover_acentos

dominios = ['com', "com.br", "xyz", "info",]

def gerar_site(nome):

    nome = remover_acentos(nome)
    nome = nome.lower().replace(" de ", "").replace(" da ", "").replace(
        " do ", "").replace(" das ", "").replace(" dos ", "").replace(" ", "")
    dominio = random.choice(dominios)
    site = f'{nome}.{dominio}'
    return site