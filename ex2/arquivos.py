"""
arquivos.py - Funções para ler e gravar arquivos JSON.

JSON é um formato de texto para guardar dados. Em Python, ele vira
dicionários ({}) e listas ([]).

TAREFA: complete as duas funções. Dicas:
    os.path.exists(caminho)        -> True se o arquivo existe
    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)                 # lê
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)   # grava
"""

import json
import os


def carregar_json(caminho, padrao=None):
    """Lê o arquivo JSON e devolve os dados.
    Se o arquivo não existir, devolve o valor 'padrao'."""
    # TODO
    raise NotImplementedError


def salvar_json(caminho, dados):
    """Grava os dados no arquivo JSON (apaga o conteúdo antigo)."""
    # TODO
    raise NotImplementedError
