import sys
import os

# Adiciona o diretório 'Controle' ao sys.path
diretorio_atual = os.path.dirname(__file__)
diretorio_pai = os.path.abspath(os.path.join(diretorio_atual, "..", "..", ".."))
diretorio_controle = os.path.abspath(os.path.join(diretorio_pai, "Controle"))
diretorio_scripts = os.path.abspath(os.path.join(diretorio_pai, "Scripts"))

if diretorio_controle not in sys.path:
    sys.path.append(diretorio_controle)

if diretorio_scripts not in sys.path:
    sys.path.append(diretorio_scripts)

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from Controle import *
from Controle.Moderno import *
import numpy as np
from scipy.linalg import expm


def sim_evolucao_erro(sistema, K, Ko, x0, e0):

    # === Configuração === #
    T = 10

    show_var = "estados"  # "saidas" / "estados" / "controles"
    estados = (
        []
    )  # indice do estado que você que observar (referência vem da matriz C, neste caso 0 corresponde à vel. horizontal)

    # === Sistema === #
    # matrizes do sistema
    A = sistema.A
    B2 = sistema.B2
    B1 = sistema.B1
    C = sistema.C
    D = sistema.D

    lbl_estados = sistema.estados
    lbl_disturbios = sistema.perturbacoes
    lbl_controle = sistema.controle
    lbl_saidas = sistema.saidas

    nx = A.shape[0]
    ny = C.shape[0]
    nw = B1.shape[1]
    nu = B2.shape[1]

    # === Contas === #
    A11 = A - B2 @ K
    A12 = B2 @ K
    A21 = np.zeros(A.shape)
    A22 = A - Ko @ C

    Lambda = np.block([[A11, A12], [A21, A22]])

    x = np.array(x0)
    e = np.array(e0)

    xe = np.concatenate((x, e))
    print(xe)
    xe_ponto = Lambda @ xe

    x_ponto = xe_ponto[: len(x)]
    e_ponto = xe_ponto[len(x) :]
    # # print(ct.damp(sys))
    # yout, t, xout = cmat.initial(sys, T, X0=X0, return_x=True)

    # if show_var == "saidas":  # mostrar saídas, matriz C
    #     if len(estados) == 0:
    #         estados = range(yout.shape[1])
    #     x = yout[:, estados]
    #     labels = lbl_saidas
    # elif show_var == "estados":  # mostrar estados, matriz A
    #     if len(estados) == 0:
    #         estados = range(xout.shape[1])
    #     x = xout[:, estados]
    #     labels = lbl_estados
    # elif show_var == "controles":
    #     if len(estados) == 0:
    #         estados = range(nu)
    #     x = -np.array(xout[:, :] @ K.transpose())
    #     labels = lbl_controle

    # # === Plot === #
    # fig = go.Figure()

    # for i in range(x.shape[1]):
    #     fig.add_trace(
    #         go.Scatter(
    #             x=t,
    #             y=x[:, i],
    #             mode="lines",
    #             name=labels[i],
    #         )
    #     )

    # fig.update_layout(
    #     title="Resposta a condição inicial",
    #     xaxis=dict(
    #         title="Tempo [s]",
    #         # range = [min(self.WSs), max(self.WSs)],
    #         # nticks = 50,
    #         # showgrid = True,
    #         # gridcolor = "lightgrey",
    #     ),
    #     yaxis=dict(
    #         title="Variáveis de " + show_var,
    #         # range = [min(self.PWs), max(self.PWs)],
    #         # dtick = 0,
    #         # tickrange = [0,1],
    #         # gridcolor = "lightgrey"
    #     ),
    #     showlegend=True,
    #     legend=dict(
    #         orientation="h",
    #         # entrywidth=70,
    #         font=dict(
    #             # family="Courier",
    #             size=10,
    #             # color="black"
    #         ),
    #         yanchor="top",
    #         y=-0.20,
    #         xanchor="center",
    #         x=0.5,
    #         # bordercolor="Black",
    #         # borderwidth=1,
    #     ),
    #     plot_bgcolor="White",
    #     paper_bgcolor="White",
    #     template="plotly_white",
    #     width=700,
    #     height=500,
    # )

    # return fig
    return Lambda


def e(sistema, K, Ko, x0, e0):
    tss = 0.001
    t = np.arange(0, 10 + tss, tss)
    x = np.array(x0)
    e = np.array(e0)

    xe = np.concatenate((x, e))

    erro0 = np.zeros((len(t), len(xe)))
    print(erro0)
    erro0[0, :] = xe
    erro2 = np.copy(erro0)

    A = sistema.A
    B2 = sistema.B2
    B1 = sistema.B1
    C = sistema.C
    D = sistema.D

    lbl_estados = sistema.estados
    lbl_disturbios = sistema.perturbacoes
    lbl_controle = sistema.controle
    lbl_saidas = sistema.saidas

    nx = A.shape[0]
    ny = C.shape[0]
    nw = B1.shape[1]
    nu = B2.shape[1]

    A11 = A - B2 @ K
    A12 = B2 @ K
    A21 = np.zeros(A.shape)
    A22 = A - Ko @ C

    Lambda = np.block([[A11, A12], [A21, A22]])

    phi_LQR = expm(Lambda * tss)

    for i in range(1, len(t)):
        erro0[i, :] = phi_LQR @ erro0[i - 1, :].T

    x_t = erro0[:, : len(x0)]  # x(t)
    e_t = erro0[:, len(x0) :]  # e(t)
    print(erro0)
    labels = lbl_estados

    # === Plot === #
    fig = go.Figure()
    # print(erro0.shape[1])
    for i in range(e_t.shape[1]):
        fig.add_trace(
            go.Scatter(
                x=t,
                y=e_t[:, i],
                mode="lines",
                name=labels[i],
            )
        )

    fig.update_layout(
        title="Evolução do erro",
        xaxis=dict(
            title="Tempo [s]",
            # range = [min(self.WSs), max(self.WSs)],
            # nticks = 50,
            # showgrid = True,
            # gridcolor = "lightgrey",
        ),
        yaxis=dict(
            title="Erro das variávies de estado",
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
            y=-0.20,
            xanchor="center",
            x=0.5,
            # bordercolor="Black",
            # borderwidth=1,
        ),
        plot_bgcolor="White",
        paper_bgcolor="White",
        template="plotly_white",
        width=700,
        height=500,
    )

    fig2 = go.Figure()
    # print(erro0.shape[1])
    for i in range(x_t.shape[1]):
        fig2.add_trace(
            go.Scatter(
                x=t,
                y=x_t[:, i],
                mode="lines",
                name=labels[i],
            )
        )

    fig2.update_layout(
        title="Evolução do erro",
        xaxis=dict(
            title="Tempo [s]",
            # range = [min(self.WSs), max(self.WSs)],
            # nticks = 50,
            # showgrid = True,
            # gridcolor = "lightgrey",
        ),
        yaxis=dict(
            title="Erro das variávies de estado",
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
            y=-0.20,
            xanchor="center",
            x=0.5,
            # bordercolor="Black",
            # borderwidth=1,
        ),
        plot_bgcolor="White",
        paper_bgcolor="White",
        template="plotly_white",
        width=700,
        height=500,
    )

    return fig, fig2, erro0


if __name__ == "__main__":
    from main import sist

    K = sist.Controlador.LQR.P.Ganhos
    Ko = sist.Observador.LQR.P.Ganhos

    x0 = [20, 4, 0, 10 / 57.3]
    e0 = 0.9 * np.ones(len(x0))
    fig, fig2, erro = e(sistema=sist.sistema, K=K, Ko=Ko, x0=x0, e0=e0)
    fig.show()
    fig.write_image("evolucao_erro_LQR.png", scale=2)
    fig2.show()
