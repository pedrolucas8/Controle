"""Trabalho - Grupo 7
Júlia Jeszensky de Menezes - 11804790
Luã de Souza Santos - 11803927
Pedro Lucas - 11894520
"""

# importando as bibliotecas necessárias
from Controle import *

# Definicao do sistema #
sist = structtype()

def_sistema(sist)

controle_moderno(sist)

# print(resultado["Observador"]["LQR"])
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
