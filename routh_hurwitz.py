# importando as bibliotecas necessárias
from bibliotecas import *


def tabela2latex(tabela):
    pass


def RH_caso_especial_1(polinomio):
    novo_polinomio = np.copy(polinomio[::-1])

    tabela, soma_mudanca_sinal, estavel = routh_hurwitz(polinomio=novo_polinomio)
    return tabela, soma_mudanca_sinal, estavel


def RH_caso_especial_2(polinomio, tabela, linha):
    # Calcula o grau do polinômio atual
    grau = len(polinomio) - 1

    # Cria um novo array para armazenar os coeficientes com zeros adicionados entre eles
    coeficientes_transformados = np.zeros(2 * grau + 1)

    # Preenche o novo array com os coeficientes originais nos índices pares
    coeficientes_transformados[::2] = polinomio

    # print(coeficientes_transformados)

    # print("linha com zeros", linha, tabela[linha, :])
    # print("linha sem zeros", linha - 1, tabela[linha - 1, :])

    grau_desejado = linha + 1
    # print("grau desejado", grau_desejado)
    tamanho_array_transformado = len(coeficientes_transformados)
    # print("tamanho array transformado", tamanho_array_transformado)
    tamanho_do_array_que_eu_quero = tamanho_array_transformado - (linha - 1)
    # print("tamanho do array que eu quero", tamanho_do_array_que_eu_quero)
    array_que_eu_quero = np.copy(
        coeficientes_transformados[:tamanho_do_array_que_eu_quero]
    )
    # print("array que eu quero", array_que_eu_quero)

    # Deriva o polinômio
    coeficientes_derivados = np.polyder(array_que_eu_quero)
    # print(coeficientes_derivados)
    coeficientes_derivados = coeficientes_derivados[::2].astype(float)
    # print("coeficientes derivados transformados", coeficientes_derivados)

    while len(tabela[linha, :]) > len(coeficientes_derivados):
        coeficientes_derivados = np.append(coeficientes_derivados, 0)
    tabela[linha, :] = coeficientes_derivados
    # print(tabela)

    return tabela


def calcula_primeiras_linhas(polinomio):
    primeira_linha = np.array([])
    segunda_linha = np.array([])
    # Selecionar elementos de índices pares
    primeira_linha = polinomio[::2].astype(float)

    # Selecionar elementos de índices ímpares
    segunda_linha = polinomio[1::2].astype(float)

    # Garante que os array tenham o mesmo tamanho
    while len(primeira_linha) > len(segunda_linha):
        segunda_linha = np.append(segunda_linha, 0)

    return (primeira_linha, segunda_linha)


def routh_hurwitz(polinomio):
    """Calculadora da tabela de Routh-Hurtwitz

    As duas condições abaixo são necessárias para o sistema ser estável, mas não são suficientes:
    * Todos os coeficientes do polinômio devem possuir o mesmo sinal
    * Nenhum dos coeficientes deve desaparecer, por exemplo, todas as potências de "s" devem estar presentes na equação característica
    Observação: Se algum polinômio satisfazer as duas condições acima, ele é chamado de Polinômio de Hurwitz.

    * O critério de Routh-Hurwitz é um teste matemático que é condição necessária e suficiente para a estabilidade de um sistema LTI.
    * Todas as raízes de uma equação característica estão no LHP (Meio Plano Esquerdo) se e somente se um certo conjunto de combinações algébricas de seus coeficientes têm o mesmo sinal

    Args:
        polinomio (array): equação característica da função de transferência da maior potência para a menor

    Retorna:
        tabela (matriz): matriz contendo a tabela de Routh-Hurwitz
        soma_mudanca_sinal (int): número de vezes que mudou o sinal na primeira colunas da tabela, a quantidade de vezes é a mesma que a quantidade de polos no RHP (Meio Plano Direito), ou seja, se o valor for diferente de zero então o sistema analisado é instável
        estavel (boleano): retorna se o sistema é estável ou não por esse critério
    """
    passou_caso_especial_2 = False
    primeira_linha, segunda_linha = calcula_primeiras_linhas(polinomio=polinomio)
    linhas = len(polinomio)
    colunas = len(primeira_linha)
    tabela = np.zeros((linhas, colunas))

    tabela[0, : len(primeira_linha)] = primeira_linha
    tabela[1, :colunas] = segunda_linha

    i = 2
    while i < linhas:
        j = 0
        while j < colunas - 1:
            if not passou_caso_especial_2:
                pass
            else:
                j -= 1
                i = linha + 1
                passou_caso_especial_2 = False

            a0 = tabela[i - 2, 0]
            a1 = tabela[i - 1, 0]
            a2 = tabela[i - 2, j + 1]
            a3 = tabela[i - 1, j + 1]
            if a1 != 0:
                coeficiente = (-1 * (a0 * a3 - a1 * a2)) / a1
                if coeficiente != -0.0:
                    tabela[i, j] = coeficiente
                else:
                    tabela[i, j] = 0
            else:
                # print(tabela)
                # print("linha que temo zero na primeira coluna:", tabela[i - 1, :])
                if np.any(tabela[i - 1, :]):
                    # print(
                    #     "to no if que verifica se tem algum valor no array na difernete de zero"
                    # )
                    tabela, soma_mudanca_sinal, estavel = RH_caso_especial_1(
                        polinomio=polinomio
                    )
                    return tabela, soma_mudanca_sinal, estavel
                else:
                    # print(
                    #     "to no else e todos os valores da linha sao zero",
                    #     tabela[i - 1, :],
                    # )
                    novo_polinomio = np.copy(tabela[i - 2, :])
                    linha = i - 1
                    # return novo_polinomio, linha, None
                    passou_caso_especial_2 = True
                    tabela = RH_caso_especial_2(
                        polinomio=novo_polinomio, tabela=tabela, linha=linha
                    )
                    j = 0
                    # return tabela, soma_mudanca_sinal, estavel
                    # print(novo_polinomio)
                    # print("todos sao zero")
            j += 1
        i += 1

    # Conta quantas vezes o sinal mudou na primeira coluna
    soma_mudanca_sinal = np.count_nonzero(np.diff(np.sign(tabela[:, 0])))

    estavel = True

    if soma_mudanca_sinal != 0:
        estavel = False
    return tabela, soma_mudanca_sinal, estavel


if __name__ == "__main__":
    polinomio = np.array([1, 2, 8, 12, 20, 16, 16])
    t, n, e = routh_hurwitz(polinomio=polinomio)
    print(t)
    print(n)
    print(e)
