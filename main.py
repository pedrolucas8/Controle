# Trabalho - Grupo 7
# Júlia Jeszensky de Menezes - 11804790
# Luã de Souza Santos - 11803927
# Pedro Lucas - 11894520

import json

# importando os modulos gerados
import controle_moderno

# importando as bibliotecas necessárias
from bibliotecas import *

# Definicao do sistema #

# Matriz de estados. x = [u, w, q, theta]'
A = np.array(
    [
        [-0.2655, -0.1235, 0.8388, -9.7925],
        [-1.4412, -3.7332, 15.2192, 0.5863],
        [-0.3795, -6.3157, -4.7475, 0],
        [0, 0, 1, 0],
    ]
)

# # Matriz de entrada de disturbios (A fazer!!)
# B1 = 0;

# Matriz de entradas de controle
B2 = np.array([[-0.6862, 0.0813], [-7.4350, 0], [-183.7447, 0.3455], [0, 0]])
(_, colunas_B2) = np.shape(B2)

# Matriz de observacao y = [u, w]'
C = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
(linhas_C, _) = np.shape(C)
# Matriz de alimentação direta
D = np.zeros((linhas_C, colunas_B2))

estados = [
    "Vel. Horizontal (u)",
    "Vel. Vertical (w)",
    "Taxa Arfagem (q)",
    "Ang. Atitude (theta)",
]
entradas = ["Def. Profundor (eta)", "Tração (tau)"]
saidas = ["Vel. Horizontal (u)", "Vel. Vertical (w)"]

sys = ct.ss(
    A,
    B2,
    C,
    D,
    inputs=entradas,
    outputs=saidas,
    states=estados,
)

resultado = dict()

resultado["A"] = A
resultado["B2"] = B2
resultado["C"] = C
resultado["D"] = D
resultado["sys_malha_aberta"] = sys


resultado = controle_moderno.controle_moderno(resultado)
# graficos(resultado)

# salvando o struct
# # Converter o dicionário para uma string JSON
# def numpy_array_to_list(resultado):
#     if isinstance(resultado, np.integer):
#         return int(resultado)
#     if isinstance(resultado, np.floating):
#         return float(resultado)
#     if isinstance(resultado, np.ndarray):
#         return resultado.tolist()
#     return json.JSONEncoder.default(resultado, None)


# json_string = json.dumps(numpy_array_to_list(resultado), indent=2)
# print(resultado)
# # C1 = eye(4);
# # [linhas_C,~] = size(C1);

# # Matriz de alimentação direta
# # D1 = zeros(linhas_C,colunas_B2);

# resultado.A = A;
# resultado.B1 = B1;
# resultado.B2 = B2;
# resultado.C = C;
# resultado.D = D;


# resultado.sys_malha_aberta = ss(A, B2, C, D,'statename',estados,...
# 'inputname',entradas,...
# 'outputname',saidas);

# resultado.FTs = tf(resultado.sys_malha_aberta);

# # CONTROLE MODERNO
# resultado = controle_moderno(resultado);

# # CONTROLE CLÁSSICO
# # resultado = controle_classico(resultado);

# # PLOT
# if plotar
#     plots(resultado)
# else
#     fprintf("Plot desabilitado \n");
# end
