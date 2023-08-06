import random
from PyFakeDados.cep import gerar_cep
from PyFakeDados.estado import gerar_estado, gerar_uf, busca_nome_uf
from PyFakeDados.municipio import gerar_municipio
from PyFakeDados.bairro import gerar_bairro
from PyFakeDados.logradouro import gerar_logradouro, gerar_numero
from PyFakeDados.telefone import gerar_telefone_fixo, gerar_telefone_celular
from PyFakeDados.email import gerar_email
from PyFakeDados.site import gerar_site
from PyFakeDados.cnpj import gerar_cnpj
from PyFakeDados.inscricao_estadual import gerar_inscricao_estadual
from PyFakeDados.utils import gerar_data
from PyFakeDados.pessoa import gerar_pessoa

LISTA_SEGMENTOS = ['Consultoria', 'Indústria', 'Comércio', 'Energia', 'Engenharia', 'Logística',
                   'Transportadora', 'Agro', 'Farmacêutica', 'Cerâmica', 'Madeireira', 'Marcenaria', 'Construtora', 'Metalurgica']


def gerar_segmento():
    return random.choice(LISTA_SEGMENTOS)


def gerar_nome_empresa(segmento=None):

    layouts = [1, 2, 3]
    palavras1 = ['Nova', 'Primeira', 'Global', 'Mega', 'Excel', 'Pro', 'Super', 'Ultra',
                 'Master', 'Max', 'Top', 'Red', 'Blue', 'Green', 'Gray', 'Sec', 'Global', ]
    palavras2 = ['Tecnologia', 'Soluções']
    palavras3 = ['S/A', 'S.A.', 'LTDA', 'Ltda.', 'EIRELI', 'ME', 'Group']

    layout = random.choice(layouts)

    if segmento is None:
        segmento = gerar_segmento()

    palavra1 = random.choice(palavras1)
    palavra2 = random.choice(palavras2)
    palavra3 = random.choice(palavras3)

    if layouts == 1:
        return f'{segmento} {palavra1} {palavra2} {palavra3}'
    elif layouts == 2:
        return f'{palavra1} {palavra2} {segmento} {palavra3}'
    elif layouts == 3:
        return f'{palavra1} {segmento} {palavra2} {palavra3}'

    return f'{segmento} {palavra1} {palavra2} {palavra3}'


def gerar_empresa(uf=None, segmento=None):

    if uf is None:
        uf = gerar_uf()

    empresa = {}
    socios = []

    nome = gerar_nome_empresa(segmento)
    cnpj = gerar_cnpj()
    inscricao_estadual = gerar_inscricao_estadual()
    data_abertura = gerar_data()
    site = gerar_site(nome)
    email = gerar_email(nome)
    cep = gerar_cep(uf)
    endereco = gerar_logradouro()
    numero = gerar_numero()
    bairro = gerar_bairro()
    municipio = gerar_municipio(uf)
    estado = busca_nome_uf(uf)
    telefone = gerar_telefone_fixo(uf)
    celular = gerar_telefone_celular(uf)

    if not nome.endswith("S.A.") and not nome.endswith("S/A") :
        socios = [gerar_pessoa() for socio in range(1, random.randint(1,5))]

    empresa = {
        "nome": nome,
        "cnpj": cnpj,
        "inscricao_estudal": inscricao_estadual,
        "data_abertura": data_abertura.strftime("%d/%m/%Y"),
        "site": site,
        "email": email,
        "cep": cep,
        "endereco": endereco,
        "numero": numero,
        "bairro": bairro,
        "municipio": municipio,
        "estado": estado,
        "uf": uf,
        "telefone": telefone,
        "celular": celular,
        "socios": socios,
    }

    return empresa
