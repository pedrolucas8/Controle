from plotly.subplots import make_subplots
import plotly.graph_objects as go
from Controle import *
from Controle.Moderno import *


def sim_inicial_malha_fechada(sistema, K):

    # === Configuração === #
    T = 10

    X0 = [0, 0, 0, 10 / 57.3]

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

    lbl_estados = sistema.estados.copy()
    lbl_disturbios = sistema.perturbacoes.copy()
    lbl_controle = sistema.controle.copy()
    lbl_saidas = sistema.saidas.copy()

    nx = A.shape[0]
    ny = C.shape[0]
    nw = B1.shape[1]
    nu = B2.shape[1]

    # === Contas === #
    F = A - B2 @ K
    Cr = C - D @ K
    B0 = np.zeros(B2.shape)
    D0 = np.zeros(D.shape)
    sys = ct.ss(F, B0, Cr, D0)
    print(ct.damp(sys))
    yout, t, xout = cmat.initial(sys, T, X0=X0, return_x=True)

    if show_var == "saidas":  # mostrar saídas, matriz C
        if len(estados) == 0:
            estados = range(yout.shape[1])
        x = yout[:, estados]
        labels = lbl_saidas
    elif show_var == "estados":  # mostrar estados, matriz A
        if len(estados) == 0:
            estados = range(xout.shape[1])
        x = xout[:, estados]
        labels = lbl_estados
    elif show_var == "controles":
        if len(estados) == 0:
            estados = range(nu)
        x = -np.array(xout[:, :] @ K.transpose())
        labels = lbl_controle

    for i in range(x.shape[1]):
        if "[rad" in labels[i]:
            x[:,i] *= 180/np.pi
            labels[i] = labels[i].replace("[rad", "[deg")
    

    # === Plot === #
    fig = go.Figure()

    for i in range(x.shape[1]):
        fig.add_trace(
            go.Scatter(
                x=t,
                y=x[:, i],
                mode="lines",
                name=labels[i],
            )
        )

    fig.update_layout(
        title="Resposta a condição inicial",
        xaxis=dict(
            title="Tempo [s]",
            # range = [min(self.WSs), max(self.WSs)],
            # nticks = 50,
            showgrid=True,  # Show major gridlines
            gridwidth=1,    # Major gridlines width
            gridcolor='#CCCCCC',  # Color of major gridlines
            minor_showgrid=True,  # Show minor gridlines
            minor_gridwidth=0.5,  # Minor gridlines width
            minor_gridcolor='#EAEAEA'  # Color of minor gridlines
        ),
        yaxis=dict(
            title="Variáveis de " + show_var,
            # range = [min(self.PWs), max(self.PWs)],
            # dtick = 0,
            # tickrange = [0,1],
            showgrid=True,  # Show major gridlines
            gridwidth=1,    # Major gridlines width
            gridcolor='#CCCCCC',  # Color of major gridlines
            minor_showgrid=True,  # Show minor gridlines
            minor_gridwidth=0.5,  # Minor gridlines width
            minor_gridcolor='#EAEAEA'  # Color of minor gridlines
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

    return fig


if __name__ == "__main__":
    # K = sist.Controlador.LQR.P.Ganhos  # type: ignore
    # K = sist.Controlador.Alocacao.P3.Ganhos # type: ignore

    # polos = np.array([-5 +10j , -5 -10j ,-0.27+0.83j, -0.27-0.83j])
    # polos = np.array([-0.20 + .20j, -0.20 - 0.20j, -4.5 + 9j, -4.5 - 9j])
    # polos = np.array([-5 + 10j, -5 - 10j, -.81 + .81j, -.81 - .81j])
    # polos = np.array([-4 + 5j, -4 - 5j, -0.5 + 0.4j, -0.5 - 0.4j])
    from main import sist

    K = sist.Controlador.LQR.P.Ganhos

    # controlador = controlador_alocacao_polos(
    #     sist.sistema.A,
    #     sist.sistema.B1,
    #     sist.sistema.B2,
    #     sist.sistema.C,
    #     sist.sistema.D,
    #     polos,
    # )
    # K = controlador.Ganhos
    fig = sim_inicial_malha_fechada(sist.sistema, K)  # type: ignore
    fig.show()
    fig.write_image("cenario_estados_LQR.png", scale=2)
