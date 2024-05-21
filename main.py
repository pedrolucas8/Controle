"""Trabalho - Grupo M
Júlia Jeszensky de Menezes - 11804790
Júlio César de Andrade Oliveira - 12873615
Luã de Souza Santos - 11803927
Pedro Lucas - 11894520
"""

# importando as bibliotecas necessárias
from Controle import *
from Scripts import *

# Definicao do sistema #
sist = get_sistema()

malha_aberta(sist)

controle_moderno(sist)

fig = Plots.plot_polos(sist.sys_malha_aberta)
fig.show()
fig.write_image("fig_polos.png", scale=2)

