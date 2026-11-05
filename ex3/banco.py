"""
banco.py - Exercício 3: histórico e ranking das batalhas no SQLite.

TAREFA: complete as funções marcadas com TODO e rode testes_ex3.py.
Use "?" nos comandos SQL e passe os valores numa tupla, como no
exercício do RPG com banco de dados.
"""

import sqlite3
from datetime import date

import arquivos

NOME_ARQUIVO = "arena.db"


def conectar(nome_arquivo=NOME_ARQUIVO):
    """Abre (ou cria) o banco e a tabela partidas. (PRONTA)"""
    conn = sqlite3.connect(nome_arquivo)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS partidas (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            jogador        TEXT NOT NULL,
            inimigo        TEXT NOT NULL,
            resultado      TEXT NOT NULL,
            turnos         INTEGER NOT NULL,
            vida_restante  INTEGER NOT NULL,
            data           TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def registrar_partida(conn, jogador, inimigo, resultado, turnos, vida_restante, data=None):
    """Grava uma partida (INSERT) e devolve o id gerado.
    Se data for None, use a data de hoje:  date.today().isoformat()  -> "2026-11-05"
    Não esqueça do conn.commit()."""
    # TODO
    raise NotImplementedError


def historico(conn, jogador):
    """Lista as partidas de UM jogador, em ordem de id.
    Cada linha: (id, inimigo, resultado, turnos, vida_restante, data)"""
    # TODO: SELECT ... FROM partidas WHERE jogador = ? ORDER BY id
    raise NotImplementedError


def contar_resultados(conn, jogador):
    """Conta vitórias, derrotas e fugas do jogador e devolve um dicionário:
        {"vitoria": 1, "derrota": 1, "fuga": 1}
    Faça com um laço for sobre historico(conn, jogador).
    (Na linha do histórico, o resultado é a posição [2].)"""
    # TODO
    raise NotImplementedError


def ranking(conn, limite=5):
    """As melhores VITÓRIAS: quem terminou com mais vida fica na frente;
    se empatar, quem venceu em menos turnos.
    Cada linha: (jogador, inimigo, turnos, vida_restante)
    Dica: WHERE resultado = 'vitoria'  ORDER BY vida_restante DESC, turnos ASC  LIMIT ?"""
    # TODO
    raise NotImplementedError


def exportar_ranking(conn, caminho, limite=5):
    """DESAFIO: grava o ranking em um arquivo JSON e devolve a lista gravada.
    Cada posição vira um dicionário:
        {"posicao": 1, "jogador": "Carla", "inimigo": "Orc", "turnos": 8, "vida_restante": 90}
    Use ranking(conn, limite) e arquivos.salvar_json(caminho, lista)."""
    # TODO
    raise NotImplementedError
