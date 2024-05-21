from ..bibliotecas import *

from plotly.subplots import make_subplots
import plotly.graph_objects as go


def plot_polos(sys):
    fig = go.Figure()
    polos = ct.pole(sys)
    # zeros = ct.zero(sys)
    fig.add_trace(go.Scatter(
        x=np.real(polos),y=np.imag(polos),
        mode = "markers",
        marker=dict(
            color='red',
            size=20,
            symbol="x-thin",
            line=dict(
                color='red',
                width=2
            )
        ),
    ))

    # fig.add_trace(go.Scatter(
    #     x=np.real(zeros),y=np.imag(zeros),
    #     mode = "markers",
    #     marker=dict(
    #         color='black',
    #         size=20,
    #         symbol="circle-open",
    #         line=dict(
    #             color='black',
    #             width=2
    #         )
    #     ),
    # ))

    fig.update_layout(
        title="Polos e Zeros",
        xaxis = dict(
            title= "Re",
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
            title="Im",
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
        showlegend=False,
        plot_bgcolor="White",
        paper_bgcolor="White",
        template = "plotly_white",
        width=700, height=500,
    )

    return fig