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
from PyFakeDados.inscricao_estudal import gerar_inscricao_estadual
from PyFakeDados.utils import gerar_data

def gerar_nome_empresa():
    segmento = ['Tecnologia', 'Soluções', 'Consultoria', 'Indústria', 'Comércio', 'Energia', 'Engenharia', 'Logística', 'Agro', 'Farmacêutica', 'Cerâmica', 'Madeireira', 'Marcenaria', 'Construtora', 'Metalurgica']
    palavra1 = ['Nova', 'Primeira', 'Global', 'Mega', 'Excel', 'Pro', 'Super', 'Ultra', 'Master', 'Max', 'Top']
    palavra2 = ['Tecnologia', 'Soluções', 'Consultoria', 'Indústria', 'Comércio', 'Energia', 'Engenharia', 'Logística', 'Agro', 'Farmacêutica']
    palavra3 = ['S/A', 'LTDA', 'Ltda.', 'EIRELI', 'ME', 'S.A.', 'Group']
    
    segmento_escolhido = random.choice(segmento)
    palavra1_escolhida = random.choice(palavra1)
    palavra2_escolhida = random.choice(palavra2)
    palavra3_escolhida = random.choice(palavra3)
    
    return f'{segmento_escolhido} {palavra1_escolhida} {palavra2_escolhida} {palavra3_escolhida}'

def gerar_empresa(uf=None):

    if uf is None:
        uf = gerar_uf()

    empresa = {}

    nome = gerar_nome_empresa()
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
    }

    return empresa
