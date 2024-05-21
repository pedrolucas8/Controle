from plotly.subplots import make_subplots
import plotly.graph_objects as go
from Controle import *
from Controle.Moderno import *


def sim_degrau_malha_aberta(sys):

    # === Configuração === #
    T = 20

    input = 0
    ref = 1 * np.pi / 180

    show_var = "estados"  # "saidas" / "estados" / "controles"
    estados = (
        []
    )  # indice do estado que você que observar (referência vem da matriz C, neste caso 0 corresponde à vel. horizontal)

    # === Sistema === #
    B2 = sys.B

    lbl_saidas = sys.output_labels
    lbl_estados = sys.state_labels
    lbl_controle = sys.input_labels

    nu = B2.shape[1]

    # === Contas === #
    yout, t, xout = cmat.step(sys, T, input=input, return_x=True)

    if show_var == "saidas":  # mostrar saídas, matriz C
        if len(estados) == 0:
            estados = range(yout.shape[1])
        x = ref * yout[:, estados, 0]
        labels = lbl_saidas
    elif show_var == "estados":  # mostrar estados, matriz A
        if len(estados) == 0:
            estados = range(xout.shape[1])
        x = ref * xout[:, estados, 0]
        labels = lbl_estados
    elif show_var == "controles":
        if len(estados) == 0:
            estados = range(nu)
        x = np.zeros((len(t), nu))
        x[:, input] += ref
        labels = lbl_controle

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
        title="Resposta a entrada degrau",
        xaxis=dict(
            title="Tempo [s]",
            # range = [min(self.WSs), max(self.WSs)],
            # nticks = 50,
            # showgrid = True,
            # gridcolor = "lightgrey",
        ),
        yaxis=dict(
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
    fig = sim_degrau_malha_aberta(sist.sys_malha_aberta)  # type: ignore
    fig.show()
    fig.write_image("sim_degrau_malha_aberta.png", scale=2)
