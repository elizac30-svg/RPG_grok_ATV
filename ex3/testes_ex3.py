"""
testes_ex3.py - Rode este arquivo para conferir o banco.py.
Os testes usam um banco em memória: o seu arena.db não é alterado.
"""

import os
import tempfile

import banco

acertos = 0
total = 0


def confere(descricao, funcao, esperado):
    global acertos, total
    total = total + 1
    try:
        obtido = funcao()
    except NotImplementedError:
        print(f"  ...  {descricao}  -> ainda não implementada")
        return
    except Exception as erro:
        print(f"  ERRO {descricao}  -> deu erro: {type(erro).__name__}: {erro}")
        return
    if obtido == esperado:
        acertos = acertos + 1
        print(f"  OK   {descricao}")
    else:
        print(f"  ERRO {descricao}  -> esperado {esperado!r}, veio {obtido!r}")


conn = banco.conectar(":memory:")
PARTIDAS = [("Ana", "Goblin", "vitoria", 4, 76, "2026-11-01"),
            ("Ana", "Orc", "derrota", 9, 0, "2026-11-02"),
            ("Bruno", "Goblin", "vitoria", 5, 76, "2026-11-02"),
            ("Bruno", "Lobo", "vitoria", 6, 40, "2026-11-03"),
            ("Ana", "Lobo", "fuga", 2, 55, "2026-11-04"),
            ("Carla", "Orc", "vitoria", 8, 90, "2026-11-04")]

print("registrar_partida")


def registra_todas():
    ids = []
    for p in PARTIDAS:
        ids.append(banco.registrar_partida(conn, *p))
    return ids


confere("as 6 partidas recebem os ids 1 a 6", registra_todas, [1, 2, 3, 4, 5, 6])


def sem_data():
    from datetime import date
    novo = banco.registrar_partida(conn, "Teste", "Goblin", "derrota", 1, 0)
    linha = conn.execute("SELECT data FROM partidas WHERE id = ?", (novo,)).fetchone()
    conn.execute("DELETE FROM partidas WHERE id = ?", (novo,))
    return linha[0] == date.today().isoformat()


confere("sem informar a data, grava a data de hoje", sem_data, True)

print("historico")
confere("historico(conn, 'Bruno')", lambda: banco.historico(conn, "Bruno"),
        [(3, "Goblin", "vitoria", 5, 76, "2026-11-02"), (4, "Lobo", "vitoria", 6, 40, "2026-11-03")])
confere("historico de quem nunca jogou é uma lista vazia", lambda: banco.historico(conn, "Zé"), [])

print("contar_resultados")
confere("contar_resultados(conn, 'Ana')", lambda: banco.contar_resultados(conn, "Ana"),
        {"vitoria": 1, "derrota": 1, "fuga": 1})

print("ranking")
confere("ranking(conn) - só vitórias, mais vida primeiro, empate: menos turnos",
        lambda: banco.ranking(conn),
        [("Carla", "Orc", 8, 90), ("Ana", "Goblin", 4, 76), ("Bruno", "Goblin", 5, 76),
         ("Bruno", "Lobo", 6, 40)])
confere("ranking(conn, limite=2)", lambda: banco.ranking(conn, limite=2),
        [("Carla", "Orc", 8, 90), ("Ana", "Goblin", 4, 76)])

print("exportar_ranking")
caminho = os.path.join(tempfile.mkdtemp(), "ranking.json")


def exporta():
    banco.exportar_ranking(conn, caminho, 1)
    with open(caminho, encoding="utf-8") as f:
        import json
        return json.load(f)


confere("exportar_ranking(conn, caminho, 1) grava o 1º lugar no JSON", exporta,
        [{"posicao": 1, "jogador": "Carla", "inimigo": "Orc", "turnos": 8, "vida_restante": 90}])

print(f"\nResultado: {acertos} de {total} testes certos.")
