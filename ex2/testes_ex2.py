"""
testes_ex2.py - Rode este arquivo para conferir arquivos.py e loja.py.
Os testes usam arquivos temporários: o seu heroi.json não é alterado.
"""

import os
import tempfile

import arquivos
import loja

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


CATALOGO = [{"nome": "Poção de Vida", "tipo": "Poção", "preco": 15},
            {"nome": "Espada Longa", "tipo": "Arma", "preco": 60}]


def heroi_teste(ouro=100, inventario=None):
    if inventario is None:
        inventario = {}
    return {"nome": "Teste", "ouro": ouro, "inventario": inventario}


print("arquivos.py")
pasta = tempfile.mkdtemp()
caminho = os.path.join(pasta, "teste.json")
confere("carregar_json de arquivo que não existe devolve o padrão",
        lambda: arquivos.carregar_json(caminho, {"vazio": True}), {"vazio": True})


def salva_e_le():
    arquivos.salvar_json(caminho, {"nome": "Zéfira", "itens": [1, 2]})
    return arquivos.carregar_json(caminho)


confere("salvar_json e depois carregar_json devolve os mesmos dados", salva_e_le,
        {"nome": "Zéfira", "itens": [1, 2]})

print("loja.buscar_item")
confere("buscar_item(CATALOGO, 'espada longa') acha a Espada Longa",
        lambda: loja.buscar_item(CATALOGO, "espada longa"), CATALOGO[1])
confere("buscar_item(CATALOGO, 'Machado') == None",
        lambda: loja.buscar_item(CATALOGO, "Machado"), None)

print("loja.comprar")


def compra_simples():
    h = heroi_teste()
    loja.comprar(h, CATALOGO, "Poção de Vida")
    return h["ouro"], h["inventario"]


def compra_tres():
    h = heroi_teste(inventario={"Poção de Vida": 1})
    loja.comprar(h, CATALOGO, "poção de vida", 3)
    return h["ouro"], h["inventario"]


def compra_sem_ouro():
    h = heroi_teste(ouro=50)
    msg = loja.comprar(h, CATALOGO, "Espada Longa")
    return h["ouro"], h["inventario"], msg.startswith("Ouro insuficiente")


confere("comprar 1 poção: ouro 85, inventário com 1", compra_simples, (85, {"Poção de Vida": 1}))
confere("comprar 3 poções tendo 1: ouro 55, inventário com 4", compra_tres, (55, {"Poção de Vida": 4}))
confere("comprar espada com 50 moedas: nada muda", compra_sem_ouro, (50, {}, True))
confere("comprar item inexistente devolve mensagem",
        lambda: loja.comprar(heroi_teste(), CATALOGO, "Machado"), "Esse item não existe na loja.")

print("loja.vender")


def venda():
    h = heroi_teste(ouro=0, inventario={"Poção de Vida": 2})
    loja.vender(h, CATALOGO, "Poção de Vida")
    return h["ouro"], h["inventario"]


def venda_tudo():
    h = heroi_teste(ouro=0, inventario={"Espada Longa": 1})
    loja.vender(h, CATALOGO, "Espada Longa")
    return h["ouro"], h["inventario"]


def venda_demais():
    h = heroi_teste(ouro=0, inventario={"Poção de Vida": 1})
    loja.vender(h, CATALOGO, "Poção de Vida", 5)
    return h["ouro"], h["inventario"]


confere("vender 1 de 2 poções (metade de 15 = 7): ouro 7, sobra 1", venda, (7, {"Poção de Vida": 1}))
confere("vender a única espada: ouro 30 e o item some do inventário", venda_tudo, (30, {}))
confere("vender 5 tendo só 1: nada muda", venda_demais, (0, {"Poção de Vida": 1}))

print(f"\nResultado: {acertos} de {total} testes certos.")
