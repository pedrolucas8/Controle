import sys

# sys.path.append("..")
from Controle import *
from Controle.Simulacao import simulacao_disturbio
from malha_aberta import malha_aberta
from controle_moderno import controle_moderno

# Definicao do sistema #
sist = structtype()

def_sistema(sist)

malha_aberta(sist)

controle_moderno(sist)
# sistema para ser simulado (malha fechada - controlador - alocacao - P1)
sys = sist.Controlador.Alocacao.P1.sys_mf
# matriz de ganhos
K = sist.Controlador.Alocacao.P1.Ganhos
# vetor de tempo (20 seg, dt = 0.1)
T = np.arange(start=0, stop=20, step=0.1)
# matriz de 'entrada' de distúrbio (inicialmente com matriz de um's)
W = np.ones((len(T), 2))

simulacao = simulacao_disturbio(sys=sys, K=K, T=T, W=W)

y_saida = simulacao.saida_observada
x_saida = simulacao.saida_estados

# comparacao entra malha aberta e fechada (primeiro estado)
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=T, y=y_saida[:, 0], mode="lines"))
fig.write_html("output_file_name.html", auto_open=True)
