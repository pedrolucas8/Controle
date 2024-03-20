from ..bibliotecas import *
from ..structtype import structtype 


def estabilidade(A):
    # A - matriz da planta do sistema
    polos, _ = np.linalg.eig(A)  # polos = autovalores de A
    if any(polos > 0):
        print("O sistema é instável: pelo menos um autovalor de A é maior que 0.")
        estavel = False
    else:
        print("O sistema é estável: nenhum autovalor de A é maior que 0.")
        estavel = True
    
    Estabilidade = structtype(
        polos = polos,
        estavel = estavel,
    )
    return Estabilidade