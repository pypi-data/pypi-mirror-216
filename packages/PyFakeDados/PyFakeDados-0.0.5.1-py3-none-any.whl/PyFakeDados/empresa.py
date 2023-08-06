import random
from PyFakeDados.nome import gerar_nome_completo
from PyFakeDados.cep import gerar_cep
from PyFakeDados.estado import gerar_estado, gerar_uf, busca_nome_uf
from PyFakeDados.municipio import gerar_municipio
from PyFakeDados.bairro import gerar_bairro
from PyFakeDados.logradouro import gerar_logradouro, gerar_numero
from PyFakeDados.telefone import gerar_telefone_fixo, gerar_telefone_celular
from PyFakeDados.email import gerar_email_empresa
from PyFakeDados.site import gerar_site
from PyFakeDados.cnpj import gerar_cnpj
from PyFakeDados.inscricao_estadual import gerar_inscricao_estadual
from PyFakeDados.utils import gerar_data
from PyFakeDados.pessoa import gerar_pessoa
from PyFakeDados.utils import remover_acentos

LISTA_SEGMENTOS = ['Consultoria', 'Indústria', 'Comércio', 'Energia', 'Engenharia', 'Logística',
                   'Transportadora', 'Agro', 'Farmacêutica', 'Cerâmica', 'Madeireira', 'Marcenaria', 'Construtora', 'Metalurgica']


def gerar_segmento():
    return random.choice(LISTA_SEGMENTOS)


def gerar_nome_empresa(segmento=None):

    layouts = [1, 2, 3, 4, 5]
    nomes = [gerar_nome_completo() for _ in range(1, 50)]
    palavras1 = ['Nova', 'Primeira', 'Global', 'Mega', 'Excel', 'Pro', 'Super', 'Ultra',
                 'Master', 'Max', 'Top', 'Red', 'Blue', 'Green', 'Gray', 'Sec', 'Global',
                 "Tech", "Soluções", "Inovação", "Global", "Digital", "Sistemas", "Estratégia",
                 "Criativa", "Negócios", "Marketing", "Web", "Inteligência", "Projetos", "Tecnologia", "Serviços",
                 "Desenvolvimento", "Software", "Gestão", "Empreendimentos", "Analytics", "Design",
                 "Comunicação", "Segurança", "Mobile", "App", "Investimentos", "Financeira",
                 "Consulting", "Vendas", "E-commerce", "Social", "Educação", "Recursos", "Saúde",
                 "Arquitetura", "Arte", "Eventos", "Imobiliária", "Alimentos",
                 "Moda", "Transporte", "Automotiva", "Ambiental", "Telecomunicações"]
    palavras2 = ['Nova', 'Primeira', 'Global', 'Mega', 'Excel', 'Pro', 'Super', 'Ultra',
                 'Master', 'Max', 'Top', 'Red', 'Blue', 'Green', 'Gray', 'Sec', 'Global',
                 "Tech", "Soluções", "Inovação", "Global", "Digital", "Sistemas", "Estratégia",
                 "Criativa", "Negócios", "Marketing", "Web", "Inteligência", "Projetos", "Tecnologia", "Serviços",
                 "Desenvolvimento", "Software", "Gestão", "Empreendimentos", "Analytics", "Design",
                 "Comunicação", "Segurança", "Mobile", "App", "Investimentos", "Financeira",
                 "Consulting", "Vendas", "E-commerce", "Social", "Educação", "Recursos", "Saúde",
                 "Arquitetura", "Arte", "Eventos", "Imobiliária", "Alimentos",
                 "Moda", "Transporte", "Automotiva", "Ambiental", "Telecomunicações"]
    palavras3 = ['S/A', 'S.A.', 'LTDA', 'Ltda.', 'EIRELI', 'ME', 'Group']

    layout = random.choice(layouts)

    if segmento is None:
        segmento = gerar_segmento()

    nome = random.choice(nomes)
    palavra1 = random.choice(palavras1)
    palavras2.remove(palavra1)
    palavra2 = random.choice(palavras2)
    palavra3 = random.choice(palavras3)

    if layout == 1:
        return f'{segmento} {palavra1} {palavra2} {palavra3}'
    elif layout == 2:
        return f'{palavra1} {palavra2} {segmento} {palavra3}'
    elif layout == 3:
        return f'{palavra1} {segmento} {palavra2} {palavra3}'
    elif layout == 4:
        return f'{nome} {segmento}'
    elif layout == 5:
        return f'{segmento} {nome}'

    return f'{segmento} {palavra1} {palavra2} {palavra3}'


def gerar_empresa(uf=None, segmento=None, force_ASCII=False, force_upper=False):

    if uf is None:
        uf = gerar_uf()

    empresa = {}
    socios = []

    nome = gerar_nome_empresa(segmento)
    cnpj = gerar_cnpj()
    inscricao_estadual = gerar_inscricao_estadual()
    data_abertura = gerar_data()
    site = gerar_site(nome)
    email = gerar_email_empresa(nome)
    cep = gerar_cep(uf)
    endereco = gerar_logradouro()
    numero = gerar_numero()
    bairro = gerar_bairro()
    municipio = gerar_municipio(uf)
    estado = busca_nome_uf(uf)
    telefone = gerar_telefone_fixo(uf)
    celular = gerar_telefone_celular(uf)

    if not nome.endswith("S.A.") and not nome.endswith("S/A"):
        socios = [gerar_pessoa() for socio in range(1, random.randint(1, 5))]

    empresa = {
        "nome": nome,
        "cnpj": cnpj,
        "inscricao_estadual": inscricao_estadual,
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

    if force_ASCII:
        for i in empresa:
            if isinstance(empresa[i], str):
                empresa[i] = remover_acentos(empresa[i])

    if force_upper:
        for i in empresa:
            if isinstance(empresa[i], str):
                empresa[i] = empresa[i].upper()

    return empresa
