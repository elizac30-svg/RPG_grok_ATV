"""
arena.py - Exercício 3: programa principal da arena.

Junta tudo o que foi feito:
  - batalha.py  (Exercício 1) faz a luta;
  - arquivos.py (Exercício 2) lê e grava JSON (herói, inimigos, ranking);
  - banco.py    (Exercício 3) guarda cada partida no banco arena.db.
"""

import arquivos
import batalha
import banco

ARQ_HEROI = "heroi.json"
ARQ_INIMIGOS = "inimigos.json"
ARQ_RANKING = "ranking.json"
POCAO = "Poção de Vida"


def escolher_inimigo(inimigos):
    """Mostra os inimigos numerados e devolve o escolhido (ou None para voltar)."""
    for i in range(len(inimigos)):
        ini = inimigos[i]
        print(f"{i + 1}. {ini['nome']:<10} vida {ini['vida_max']:>3}  ataque {ini['ataque']:>2}  "
              f"defesa {ini['defesa']:>2}  recompensa {ini['recompensa']:>3}")
    texto = input("Número do inimigo (Enter = voltar): ").strip()
    if texto.isdigit() and 1 <= int(texto) <= len(inimigos):
        return inimigos[int(texto) - 1]
    return None


def lutar(conn, heroi, inimigo):
    """Faz uma batalha, registra no banco e atualiza o herói (poções e ouro)."""
    # dict(...) faz uma CÓPIA: a vida do herói e do inimigo volta cheia na próxima luta
    lutador = dict(heroi)
    lutador["vida"] = heroi["vida_max"]
    oponente = dict(inimigo)
    oponente["vida"] = inimigo["vida_max"]

    pocoes = heroi["inventario"].get(POCAO, 0)
    final = batalha.batalha(lutador, oponente, pocoes)

    banco.registrar_partida(conn, heroi["nome"], inimigo["nome"], final["resultado"],
                            final["turnos"], final["vida_restante"])

    # poções usadas saem do inventário
    if final["pocoes"] > 0:
        heroi["inventario"][POCAO] = final["pocoes"]
    elif POCAO in heroi["inventario"]:
        del heroi["inventario"][POCAO]

    if final["resultado"] == "vitoria":
        heroi["ouro"] = heroi["ouro"] + inimigo["recompensa"]
        print(f"Você ganhou {inimigo['recompensa']} moedas! Agora tem {heroi['ouro']}.")
    arquivos.salvar_json(ARQ_HEROI, heroi)


def mostrar_ranking(conn):
    linhas = banco.ranking(conn)
    if not linhas:
        print("Nenhuma vitória registrada ainda.")
    posicao = 1
    for jogador, inimigo, turnos, vida in linhas:
        print(f"{posicao}º {jogador:<10} venceu {inimigo:<10} com {vida:>3} de vida em {turnos} turnos")
        posicao = posicao + 1


def main():
    heroi = arquivos.carregar_json(ARQ_HEROI)
    if heroi is None:
        print("Não achei o heroi.json. Copie o seu herói do Exercício 2 para esta pasta.")
        return
    inimigos = arquivos.carregar_json(ARQ_INIMIGOS, [])
    conn = banco.conectar()

    while True:
        print(f"\n===== ARENA ===== ({heroi['nome']}, {heroi['ouro']} moedas, "
              f"{heroi['inventario'].get(POCAO, 0)} poções)")
        print("1 - Lutar")
        print("2 - Meu histórico")
        print("3 - Ranking")
        print("4 - Exportar ranking para JSON")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            inimigo = escolher_inimigo(inimigos)
            if inimigo is not None:
                lutar(conn, heroi, inimigo)
        elif opcao == "2":
            for id, inimigo, resultado, turnos, vida, data in banco.historico(conn, heroi["nome"]):
                print(f"#{id} {data}  {inimigo:<10} {resultado:<8} {turnos} turnos, vida {vida}")
            print(banco.contar_resultados(conn, heroi["nome"]))
        elif opcao == "3":
            mostrar_ranking(conn)
        elif opcao == "4":
            lista = banco.exportar_ranking(conn, ARQ_RANKING)
            print(f"{len(lista)} posições gravadas em {ARQ_RANKING}.")
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

    conn.close()


if __name__ == "__main__":
    main()
