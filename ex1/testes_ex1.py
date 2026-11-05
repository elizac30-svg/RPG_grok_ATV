"""
testes_ex1.py - Rode este arquivo para conferir as suas funções do batalha.py.
Cada linha mostra OK (certo) ou ERRO (com o valor esperado e o que veio).
"""

import batalha

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


print("calcular_dano")
confere("calcular_dano(18, 3) == 15", lambda: batalha.calcular_dano(18, 3), 15)
confere("calcular_dano(18, 3, True) == 30 (crítico dobra)", lambda: batalha.calcular_dano(18, 3, True), 30)
confere("calcular_dano(5, 12) == 1 (mínimo 1)", lambda: batalha.calcular_dano(5, 12), 1)
confere("calcular_dano(5, 12, critico=True) == 2", lambda: batalha.calcular_dano(5, 12, critico=True), 2)

print("aplicar_dano")
confere("aplicar_dano(60, 15) == 45", lambda: batalha.aplicar_dano(60, 15), 45)
confere("aplicar_dano(10, 15) == 0 (não fica negativa)", lambda: batalha.aplicar_dano(10, 15), 0)

print("curar")
confere("curar(50, 100) == 80 (cura padrão 30)", lambda: batalha.curar(50, 100), 80)
confere("curar(90, 100) == 100 (não passa do máximo)", lambda: batalha.curar(90, 100), 100)
confere("curar(50, 100, cura=10) == 60", lambda: batalha.curar(50, 100, cura=10), 60)

print("barra_de_vida")
confere("barra_de_vida(60, 100)", lambda: batalha.barra_de_vida(60, 100), "[######----] 60/100")
confere("barra_de_vida(0, 80)", lambda: batalha.barra_de_vida(0, 80), "[----------] 0/80")
confere("barra_de_vida(45, 60, tamanho=4)", lambda: batalha.barra_de_vida(45, 60, tamanho=4), "[###-] 45/60")

print("classificar_resultado")
confere("classificar_resultado(0, 100)", lambda: batalha.classificar_resultado(0, 100), "Derrota")
confere("classificar_resultado(100, 100)", lambda: batalha.classificar_resultado(100, 100), "Vitória perfeita")
confere("classificar_resultado(50, 100)", lambda: batalha.classificar_resultado(50, 100), "Vitória")
confere("classificar_resultado(20, 100)", lambda: batalha.classificar_resultado(20, 100), "Vitória apertada")

print(f"\nResultado: {acertos} de {total} testes certos.")
