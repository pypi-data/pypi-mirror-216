import random

prefixos = [
        'Alto', 'Baixo', 'Vila', 'Nova', 'Bela', 'Jardim', 'São', 'Santa', 'Bom', 'Grande',
        'Sol', 'Mar', 'Cidade', 'Campo', 'Parque', 'Mira', 'Floresta', 'Canto', 'Lagoa', 'Praia',
        'Verde', 'Dourado', 'Ouro', 'Monte', 'Vista', 'Primavera', 'Cipreste', 'Sereno', 'Vento',
        'Porto', 'Pedra', 'Aurora', 'Brisa', 'Serrano', 'Sol Nascente', 'Maravilha', 'Celestial', 'Rio',
        'Vale', 'Aconchego', 'Harmonia', 'Eterno', 'Sorriso', 'Céu Azul', 'Sonho', 'Alegria', 'Encantamento',
        'Inspiração', 'Doce Lar', 'Azul', 'Estrela', 'Canto do Pássaro'
    ]

sufixos = ['Vista', 'Flores', 'Alegre', 'Verde', 'Luz', 'Sol', 'Mar', 'Norte', 'Sul', 'Leste', 'Oeste']

def gerar_bairro():
    
    prefixo = random.choice(prefixos)
    sufixo = random.choice(sufixos)
    
    return f'{prefixo} {sufixo}'
