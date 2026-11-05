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
