import random

SEXO_MASCULINO = 'M'
SEXO_FEMININO = 'F'

LISTA_SEXO = [SEXO_MASCULINO, SEXO_FEMININO]

LISTA_NOMES_MASCULINOS = [
    "Alex", "Bernardo", "Caio", "Daniel", "Eduardo", "Felipe", "Gabriel", "Henrique",
    "Igor", "João", "Kauã", "Leonardo", "Matheus", "Nathan", "Otávio", "Pedro",
    "Rafael", "Samuel", "Thiago", "Vitor", "Wagner", "Xavier", "Yuri", "Zélio",
    "André", "Bruno", "Carlos", "Diego", "Erick", "Fernando", "Gustavo", "Hugo",
    "Ícaro", "Jonathan", "Klaus", "Lucas", "Márcio", "Nícolas", "Orlando", "Paulo",
    "Ricardo", "Sérgio", "Túlio", "Ulisses", "Valdo", "Walter", "Xande", "Yan", "Zeca"
]

LISTA_NOMES_FEMININOS = [
    "Alice", "Bianca", "Carolina", "Daniela", "Eduarda", "Fernanda", "Gabriela", "Helena",
    "Isabela", "Júlia", "Kamila", "Larissa", "Mariana", "Natália", "Olívia", "Patrícia",
    "Raquel", "Sara", "Tatiana", "Valentina", "Wendy", "Ximena", "Yasmin", "Zara",
    "Amanda", "Bruna", "Camila", "Débora", "Eloá", "Fátima", "Giovana", "Heloísa",
    "Isis", "Jéssica", "Karina", "Lara", "Mirella", "Natasha", "Olga", "Priscila",
    "Rafaela", "Sabrina", "Talita", "Úrsula", "Vitória", "Wanda", "Xuxa", "Yara", "Zilda"
]

SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Pereira", "Rodrigues", "Ferreira", "Almeida",
    "Costa", "Gomes", "Martins", "Rocha", "Ribeiro", "Carvalho", "Melo", "Sousa",
    "Alves", "Pinto", "Cardoso", "Teixeira", "Nascimento", "Lima", "Araújo", "Fernandes",
    "Cavalcanti", "Mendes", "Barbosa", "Dias", "Cunha", "Moreira", "Correia", "Castro",
    "Monteiro", "Sales", "Reis", "Tavares", "Andrade", "Moura", "Freitas", "Santana",
    "Marques", "Bezerra", "Vieira", "Freire", "Farias", "Gonçalves", "Vargas", "Ramos",
    "Pinheiro", "Lopes", "Campos", "Brito", "Montenegro", "Macedo", "Morais", "Viana",
    "Coutinho", "Leal", "Mota", "Maia", "Pacheco", "Peixoto", "Junqueira", "Machado",
    "Dantas", "Fonseca", "Azevedo", "Barros", "Miranda", "Mourão", "Valente", "Xavier",
    "Zanetti", "Amorim", "Borges", "Diniz", "Fraga", "Godoy", "Horta", "Jardim",
    "Klein", "Luz", "Nogueira", "Otero", "Parreira", "Quintana", "Rangel", "Sampaio",
    "Toledo", "Uribe", "Vasconcelos", "Wanderley", "Ximenes", "Yoshida", "Zimmermann"
]

def gerar_sexo():
    return random.choice(LISTA_SEXO)

def gerar_nome(sexo=None):
    
    if sexo is None:
        sexo = gerar_sexo()

    if sexo == 'M':
        nome = random.choice(LISTA_NOMES_MASCULINOS)
    elif sexo == 'F':
        nome = random.choice(LISTA_NOMES_FEMININOS)
    else:
        raise ValueError("Sexo inválido. Use 'M' para masculino ou 'F' para feminino.")
    
    return f"{nome}"

def gerar_sobrenome():
    return random.choice(SOBRENOMES)

def gerar_nome_completo(sexo=None):

    if sexo is None:
        sexo = gerar_sexo()

    nome = gerar_nome(sexo=sexo)
    sobrenome = gerar_sobrenome()
    nome_completo = f"{nome} {sobrenome}"

    return nome_completo

def gerar_nome_com_filiacao():

    nome_mae = gerar_nome_completo(sexo='F')
    nome_pai = gerar_nome_completo(sexo='M')

    sobrenome_mae = nome_mae.split().pop()
    sobrenome_pai = nome_pai.split().pop()

    nome = gerar_nome()
    nome = f"{nome} {sobrenome_mae} {sobrenome_pai}"

    return nome, nome_mae, nome_pai