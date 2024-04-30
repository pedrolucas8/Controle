# Exemplo da aula do Trigo (adaptado)

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from Controle import *
from Controle.Moderno import *


# === Configuração === #
T = 10  # tempo da simulação

input = 0 # variável de controle para a simulação
ref = .5  # valor da referência; amplitude do degrau (ex. 3 m/s)


# === Sistema === #
# matrizes do sistema
W0 = 2*np.pi / 5
ps = [-2*W0 , -2.01*W0]

A  = np.matrix([
    [0,1],
    [-W0**2,0],
])
B2 = np.matrix([
    [0],
    [1],
])
B1 = np.matrix([
    [0],
    [0],
])
C  = np.matrix([
    [1,0],
])
D  = np.matrix([
    [0],
])

lbl_estados = ["θ","θ'"]
lbl_disturbios = []
lbl_controle = ["τ"]
lbl_saidas = ["θ"]

nx = A.shape[0]
ny = C.shape[0]
nw = B1.shape[1]
nu = B2.shape[1]

# === Contas === #
alocacao = controlador_alocacao_polos(A, B1, B2, C, D, ps)
K = alocacao.Ganhos

seguidor = seguidor_constante(A, B1, B2, C, D, K)
Nx = seguidor.Nx
Nu = seguidor.Nu

N = K@Nx + Nu

Ar = A - B2@K
Br = B2@N
Cr = C - D@K
Dr = D@N

sys = ct.ss(Ar, Br, Cr, Dr)
y_saida, t, x_saida = cmat.step(sys,T, input=input, return_x=True)
x_saida = ref * x_saida
u = - np.array(x_saida @ K.transpose())[:,0]

# === Plot === #

fig = go.Figure()

for i in range(0,x_saida.shape[1]):
    fig.add_trace(go.Scatter(
        x=t, y=x_saida[:,i],
        mode = "lines",
        name = lbl_estados[i],
    ))

fig.add_trace(go.Scatter(
    x=t, y=u,
    mode = "lines",
    name = lbl_controle[0],
))

fig.update_layout(
    title="Simulação seguidor constante",
    xaxis = dict(
        title= "Tempo [s]",
        # range = [min(self.WSs), max(self.WSs)],
        # nticks = 50,
        # showgrid = True,
        # gridcolor = "lightgrey",
    ),
    yaxis = dict(
        title="Variáveis",
        # range = [min(self.PWs), max(self.PWs)],
        # dtick = 0,
        # tickrange = [0,1],
        # gridcolor = "lightgrey"
    ),

    showlegend=True,
    legend=dict(
        orientation="h",
        # entrywidth=70,
        font=dict(
            # family="Courier",
            size=10,
            # color="black"
        ),

        yanchor="top",
        y=-.20,
        xanchor="center",
        x=0.5,

        # bordercolor="Black",
        # borderwidth=1,
    ),

    plot_bgcolor="White",
    paper_bgcolor="White",
    template = "plotly_white",
    width=700, height=500,
)

fig.show()
