from plotly.subplots import make_subplots
import plotly.graph_objects as go
from Controle import *
from Controle.Moderno import *


def sim_seguidor_constante(sistema,K):

    # === Configuração === #
    muda_saida = False
    T = 12  # tempo da simulação
    
    input = 0 # variável de controle para a simulação
    ref = 1 # valor da referência; amplitude do degrau (ex. 3 m/s)


    show_var = "estados" # "saidas" / "estados" / "controles"
    estados = []  # indice do estado que você que observar (referência vem da matriz C, neste caso 0 corresponde à vel. horizontal)
    



    # === Sistema === #
    # matrizes do sistema
    A  = sistema.A
    B2 = sistema.B2
    B1 = sistema.B1
    C  = sistema.C
    D  = sistema.D

    lbl_estados = sistema.estados.copy()
    lbl_disturbios = sistema.perturbacoes.copy()
    lbl_controle = sistema.controle.copy()
    lbl_saidas = sistema.saidas.copy()

    nx = A.shape[0]
    ny = C.shape[0]
    nw = B1.shape[1]
    nu = B2.shape[1]

    if muda_saida:
        C = np.matrix([
            [1,0,0,0],
            [0,0,0,1],
        ])
        lbl_saidas[1] = lbl_estados[3]

    # === Contas === #
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

    if show_var=="saidas": # mostrar saídas, matriz C
        if len(estados)==0:
            estados = range(y_saida.shape[1])
        y = ref * y_saida[:,estados,0]
        lbl = lbl_saidas
    elif show_var=="estados": # mostrar estados, matriz A
        if len(estados)==0:
            estados = range(x_saida.shape[1])
        y = ref * x_saida[:,estados,0]
        lbl = lbl_estados
    elif show_var=="controles":
        if len(estados)==0:
            estados = range(K.shape[0])
        xr = np.zeros(ny)
        xr[input] = ref
        u = - x_saida[:,:,0] @ K.transpose() + N @ xr
        y = ref * np.array(u[:,estados])
        lbl = lbl_controle

    for i in range(y.shape[1]):
        if "[rad" in lbl[i]:
            y[:,i] *= 180/np.pi
            lbl[i] = lbl[i].replace("[rad", "[deg")

    # === Plot === #

    fig = go.Figure()

    for i in range(0,y.shape[1]):
        fig.add_trace(go.Scatter(
            x=t, y=y[:,i],
            mode = "lines",
            name = lbl[i],
        ))
    
    fig.update_layout(
        title="Simulação seguidor constante",
        xaxis = dict(
            title= "Tempo [s]",
            # range = [min(self.WSs), max(self.WSs)],
            # nticks = 50,
            showgrid=True,  # Show major gridlines
            gridwidth=1,    # Major gridlines width
            gridcolor='#CCCCCC',  # Color of major gridlines
            minor_showgrid=True,  # Show minor gridlines
            minor_gridwidth=0.5,  # Minor gridlines width
            minor_gridcolor='#EAEAEA'  # Color of minor gridlines
        ),
        yaxis = dict(
            title="Variáveis",
            # range = [min(self.PWs), max(self.PWs)],
            # dtick = 0,
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
    fig = sim_seguidor_constante(sist.sistema,K) # type: ignore
    fig.show()
    fig.write_image("sim_seguidor_constante.png", scale=2)