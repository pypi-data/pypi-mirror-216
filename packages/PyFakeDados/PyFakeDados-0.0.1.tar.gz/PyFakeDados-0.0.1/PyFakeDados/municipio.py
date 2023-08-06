import csv
import random
import os
from pathlib import Path
from PyFakeDados.estado import gerar_uf

FILE_MUNICIPIOS = os.path.join(Path(__file__).resolve().parent, "src", "municipios.csv") 

def municipios_para_lista():

    municipios = []
    
    with open(FILE_MUNICIPIOS, 'r', encoding='utf-8') as file:
        content = csv.reader(file, delimiter=';')
        for line in content:
            uf = line[2]
            mun = line[3]
            municipios.append([uf, mun])
    
    return municipios

def municipios_para_dict():

    municipios = {}
    
    with open(FILE_MUNICIPIOS, 'r', encoding='utf-8') as file:
        
        content = csv.reader(file, delimiter=';')
        
        for index, line in enumerate(content):

            if index == 0:
                continue
            
            uf = line[2]
            mun = line[3]
            
            if uf not in municipios:
                municipios[uf] = []
            municipios[uf].append(mun)
    
    return municipios

LISTA_MUNICIPIO = municipios_para_lista()

DICT_MUNICIPIO = municipios_para_dict()

def gerar_municipio(uf=None):

    if uf is None:
        uf = gerar_uf()

    if uf.upper() not in DICT_MUNICIPIO:
        raise ValueError("UF inválida.")
    
    municipios = DICT_MUNICIPIO[uf]
    municipio = random.choice(municipios)

    return municipio
