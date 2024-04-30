from plotly.subplots import make_subplots
import plotly.graph_objects as go
from Controle import *
from Controle.Moderno import *

def sim_seguidor_variavel(sistema, K):

    # === Configuração === #
    T = 30
    feedback_disturbios = True
    feedback_referencia = True

    # estado inicial
    x0 = np.array([0,0,0,0])

    # modelo de distúrbio
    Ww = 2*np.pi / 3
    Aw = np.matrix([
        [0,1],
        [-Ww**2,0],
    ]) # xw1 = sin(Ww*t)
    xw0 = .1 *np.array([0,Ww])

    # referência variante no tempo
    Wr = 2*np.pi / 10
    Ar = np.matrix([
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,-Wr**2],
        [0,0,1,0],
    ])
    xr0 = 5*np.pi/180 *np.array([0,0,Wr,0])
    
    # função de penalização dos erros
    C1 = np.matrix([
        [0,0,0,1],
        [0,0,1,0],
        [0,0,1,1],
    ]) # -> C_barra


    

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

    nx = A.shape[0]
    ny = C.shape[0]
    nw = B1.shape[1]
    nu = B2.shape[1]
    nr = nx

    # === Contas === #
    # matriz de ganhos para distúrbio e referência
    seguidor = seguidor_variavel(A, B1, B2, C, D, K, Ar, C1)
    Ke = seguidor.Kex

    if not feedback_disturbios:
        Ke[:,:nw] = np.zeros((nu,nw))
    if not feedback_referencia:
        Ke[:,nw:] = np.zeros((nu,nr))

    # matriz da dinâmica das variáveis exógenas (distúrbio e referência)
    Ax = np.zeros((nw,nr))
    Ao = np.vstack((
        np.hstack(( Aw            , Ax )),
        np.hstack(( Ax.transpose(), Ar ))
    )) # [Aw Ax;Ax Ar]

    # matriz da dinâmica das variáveis de estado
    Ay = np.hstack((B1, B2@K))-B2@Ke
    
    # matriz do sistema fechado completo
    Ax = np.zeros((nw+nr,nx))
    AT = np.vstack((
            np.hstack((A-B2@K, Ay)),
            np.hstack((Ax, Ao))
    )) # -> A_barra

    # simulação
    xTo = np.concatenate((x0,xw0,xr0))
    xTo = np.matrix(xTo).transpose()
    sys = ct.ss(AT,xTo,np.identity(AT.shape[0]),np.zeros(xTo.shape))
    y,t = cmat.initial(sys,T,X0=xTo)

    # === Plot === #

    fig = go.Figure()

    for i in range(0,nx):
        fig.add_trace(go.Scatter(
            x=t, y=y[:,i].flatten(),
            mode = "lines",
            name = lbl_estados[i],
        ))
        fig.add_trace(go.Scatter(
            x=t, y=y[:,nx+nw+i].flatten(),
            mode = "lines",
            name = "ref:"+lbl_estados[i],
            line = dict(
                # color='royalblue', 
                # width=4, 
                dash='dash',
            ),
        ))
    
    fig.update_layout(
        title="Simulação seguidor variável",
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
    K = sist.Controlador.Alocacao.P5.Ganhos # type: ignore
    fig = sim_seguidor_variavel(sist.sistema,K) # type: ignore
    fig.show()
    fig.write_image("sim_seguidor_variavel.png", scale=2)