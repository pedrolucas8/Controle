from plotly.subplots import make_subplots
import plotly.graph_objects as go
from Controle import *
from Controle.Moderno import *


def sim_degrau_malha_aberta(sys):

    # === Configuração === #
    T = 15
    dt = .01
    input = 0





    # === Contas === #
    t = np.arange(start=0, stop=T, step=dt)
    yout, t, xout = cmat.step(sys=sys, T=t, return_x=True, input=input)
    labels = sys.output_labels + sys.state_labels + sys.input_labels
    yout = yout[:,:,0]
    xout = xout[:,:,0]
    x = np.hstack([yout,xout])

    # === Plot === #
    fig = go.Figure()

    for i in range(x.shape[1]):
        fig.add_trace(go.Scatter(
            x=t, y=x[:,i],
            mode = "lines",
            name = labels[i],
        ))
    
    fig.update_layout(
        title="Resposta a entrada degrau",
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
    fig = sim_degrau_malha_aberta(sist.sys_malha_aberta) # type: ignore
    fig.show()
    fig.write_image("degrau_malha_aberta.png", scale=2)