"""
main.py - Exercício 2: loja do jogo.

Usa os módulos arquivos.py (JSON) e loja.py (regras da loja).
O herói fica salvo no arquivo heroi.json: ao fechar e abrir de novo,
o ouro e o inventário continuam iguais.
"""

import arquivos
import loja

ARQ_CATALOGO = "catalogo.json"
ARQ_HEROI = "heroi.json"

HEROI_NOVO = {"nome": "Gork", "ouro": 100, "vida": 100, "vida_max": 100,
              "ataque": 18, "defesa": 5, "inventario": {}}


def ler_quantidade():
    texto = input("Quantidade (Enter = 1): ").strip()
    if texto == "":
        return 1
    if texto.isdigit():
        return int(texto)
    return 0                     # loja.comprar/vender vão recusar


def main():
    catalogo = arquivos.carregar_json(ARQ_CATALOGO, [])
    heroi = arquivos.carregar_json(ARQ_HEROI, HEROI_NOVO)

    while True:
        print("\n===== LOJA =====")
        print("1 - Ver catálogo")
        print("2 - Ver inventário")
        print("3 - Comprar")
        print("4 - Vender")
        print("0 - Salvar e sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            loja.mostrar_catalogo(catalogo)
        elif opcao == "2":
            loja.mostrar_inventario(heroi)
        elif opcao == "3":
            nome = input("Nome do item: ")
            print(loja.comprar(heroi, catalogo, nome, ler_quantidade()))
        elif opcao == "4":
            nome = input("Nome do item: ")
            print(loja.vender(heroi, catalogo, nome, ler_quantidade()))
        elif opcao == "0":
            arquivos.salvar_json(ARQ_HEROI, heroi)
            print("Jogo salvo em", ARQ_HEROI)
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
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
    if data is None:
        data = date.today().isoformat()

    cursor = conn.execute(
        """
        INSERT INTO partidas (jogador, inimigo, resultado, turnos, vida_restante, data)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (jogador, inimigo, resultado, turnos, vida_restante, data),
    )
    conn.commit()
    return cursor.lastrowid


def historico(conn, jogador):
    """Lista as partidas de UM jogador, em ordem de id.
    Cada linha: (id, inimigo, resultado, turnos, vida_restante, data)"""
    cursor = conn.execute(
        """
        SELECT id, inimigo, resultado, turnos, vida_restante, data
        FROM partidas
        WHERE jogador = ?
        ORDER BY id
        """,
        (jogador,),
    )
    return cursor.fetchall()


def contar_resultados(conn, jogador):
    """Conta vitórias, derrotas e fugas do jogador e devolve um dicionário:
        {"vitoria": 1, "derrota": 1, "fuga": 1}
    Faça com um laço for sobre historico(conn, jogador).
    (Na linha do histórico, o resultado é a posição [2].)"""
    contagem = {"vitoria": 0, "derrota": 0, "fuga": 0}
    for linha in historico(conn, jogador):
        resultado = linha[2]
        if resultado in contagem:
            contagem[resultado] = contagem[resultado] + 1
    return contagem


def ranking(conn, limite=5):
    """As melhores VITÓRIAS: quem terminou com mais vida fica na frente;
    se empatar, quem venceu em menos turnos.
    Cada linha: (jogador, inimigo, turnos, vida_restante)
    Dica: WHERE resultado = 'vitoria'  ORDER BY vida_restante DESC, turnos ASC  LIMIT ?"""
    cursor = conn.execute(
        """
        SELECT jogador, inimigo, turnos, vida_restante
        FROM partidas
        WHERE resultado = 'vitoria'
        ORDER BY vida_restante DESC, turnos ASC
        LIMIT ?
        """,
        (limite,),
    )
    return cursor.fetchall()


def exportar_ranking(conn, caminho, limite=5):
    """DESAFIO: grava o ranking em um arquivo JSON e devolve a lista gravada.
    Cada posição vira um dicionário:
        {"posicao": 1, "jogador": "Carla", "inimigo": "Orc", "turnos": 8, "vida_restante": 90}
    Use ranking(conn, limite) e arquivos.salvar_json(caminho, lista)."""
    melhores = ranking(conn, limite)
    lista_ranking = []

    for i, linha in enumerate(melhores, start=1):
        item = {
            "posicao": i,
            "jogador": linha[0],
            "inimigo": linha[1],
            "turnos": linha[2],
            "vida_restante": linha[3],
        }
        lista_ranking.append(item)

    arquivos.salvar_json(caminho, lista_ranking)
    return lista_ranking
