import random
from datetime import datetime, timedelta
from PyFakeDados.nome import gerar_sexo, gerar_nome, gerar_sobrenome, gerar_nome_completo, gerar_nome_com_filiacao
from PyFakeDados.cep import gerar_cep
from PyFakeDados.estado import gerar_estado, gerar_uf, busca_nome_uf
from PyFakeDados.municipio import gerar_municipio
from PyFakeDados.bairro import gerar_bairro
from PyFakeDados.logradouro import gerar_logradouro, gerar_numero
from PyFakeDados.telefone import gerar_telefone_fixo, gerar_telefone_celular
from PyFakeDados.email import gerar_email, gerar_email_pessoa
from PyFakeDados.senha import gerar_senha, gerar_senha_numerica
from PyFakeDados.site import gerar_site
from PyFakeDados.cpf import gerar_cpf
from PyFakeDados.ctps import gerar_ctps
from PyFakeDados.pis import gerar_pis
from PyFakeDados.utils import gerar_data, gerar_data_nascimento

def gerar_pessoa(uf=None, mask=False, idade=None, recem_nascido=False):

    if uf is None:
        uf = gerar_uf()

    if idade is None:
        
        idade_min = 1
        idade_max = 99

        if recem_nascido:
            idade_min = 0

        idade = random.randint(idade_min, idade_max)

    pessoa = {}
    data_nascimento = gerar_data_nascimento(idade)
    
    sexo = gerar_sexo()
    nome, mae, pai = gerar_nome_com_filiacao()
    cpf = gerar_cpf(mask=mask)
    ctps = gerar_ctps()
    pis = gerar_pis()
    data_nascimento = data_nascimento
    site = gerar_site(nome)
    email = gerar_email_pessoa(nome)
    senha = gerar_senha_numerica()
    senha_forte = gerar_senha(16)
    cep = gerar_cep(uf, mask=mask)
    endereco = gerar_logradouro()
    numero = gerar_numero()
    bairro = gerar_bairro()
    municipio = gerar_municipio(uf)
    estado = busca_nome_uf(uf)
    telefone = gerar_telefone_fixo(uf, mask=mask)
    celular = gerar_telefone_celular(uf)

    pessoa = {
        "sexo": sexo,
        "nome": nome,
        "mae": mae,
        "pai": pai,
        "cpf": cpf,
        "ctps": ctps,
        "pis": pis,
        "data_nascimento": data_nascimento.strftime("%d/%m/%Y"),
        "site": site,
        "email": email,
        "senha": senha,
        "senha_forte": senha_forte,
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

    return pessoa
