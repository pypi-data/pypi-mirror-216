import random
import string

def gerar_senha(tamanho=8):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return senha

def gerar_senha_numerica(tamanho=6):
    caracteres = [0,1,2,3,4,5,6,7,8,9]
    senha = ''.join(str(random.choice(caracteres)) for _ in range(tamanho))
    return senha