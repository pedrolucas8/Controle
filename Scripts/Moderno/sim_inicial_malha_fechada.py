from plotly.subplots import make_subplots
import plotly.graph_objects as go
from Controle import *
from Controle.Moderno import *


def sim_inicial_malha_fechada(sistema,K):

    # === Configuração === #
    T = 20

    X0 = [
        0,
        0,
        0,
        10/57.3
    ]

    show_var = "saidas" # "saidas" / "estados" / "controles"
    estados = []  # indice do estado que você que observar (referência vem da matriz C, neste caso 0 corresponde à vel. horizontal)
    



    # === Sistema === #
    # matrizes do sistema
    A  = sistema.A
    B2 = sistema.B2
    B1 = sistema.B1
    C  = sistema.C
    D  = sistema.D

    lbl_estados = sistema.estados
    lbl_disturbios = sistema.perturbacoes
    lbl_controle = sistema.controle
    lbl_saidas = sistema.saidas

    nx = A.shape[0]
    ny = C.shape[0]
    nw = B1.shape[1]
    nu = B2.shape[1]

    # === Contas === #
    F = A - B2@K
    Cr = C - D@K
    B0 = np.zeros(B2.shape)
    D0 = np.zeros(D.shape)
    sys = ct.ss(F, B0, Cr, D0)
    yout, t, xout = cmat.initial(sys,T, X0=X0, return_x=True)

    if show_var=="saidas": # mostrar saídas, matriz C
        if len(estados)==0:
            estados = range(yout.shape[1])
        x = yout[:,estados]
        labels = lbl_saidas
    elif show_var=="estados": # mostrar estados, matriz A
        if len(estados)==0:
            estados = range(xout.shape[1])
        x = xout[:,estados]
        labels = lbl_estados
    elif show_var=="controles":
        if len(estados)==0:
            estados = range(nu)
        x = - np.array(xout[:,:] @ K.transpose())
        labels = lbl_controle

    # === Plot === #
    fig = go.Figure()

    for i in range(x.shape[1]):
        fig.add_trace(go.Scatter(
            x=t, y=x[:,i],
            mode = "lines",
            name = labels[i],
        ))
    
    fig.update_layout(
        title="Resposta a condição inicial",
        xaxis = dict(
            title= "Tempo [s]",
            # range = [min(self.WSs), max(self.WSs)],
            # nticks = 50,
            # showgrid = True,
            # gridcolor = "lightgrey",
        ),
        yaxis = dict(
            title="Variáveis de estado",
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

    return fig



if __name__=="__main__":
    K = sist.Controlador.LQR.P.Ganhos # type: ignore
    fig = sim_inicial_malha_fechada(sist.sistema,K) # type: ignore
    fig.show()
    fig.write_image("sim_inicial_malha_fechada.png", scale=2)