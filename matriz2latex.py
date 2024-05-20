import numpy as np
from main import sist


def matriz2latex(M, decimais=None):
    if M.ndim == 1:
        M = np.array([M])
    linhas, colunas = M.shape
    string_matrix = "\\begin{equation}\n\\begin{bmatrix}\n"

    for l in range(linhas):
        string_linha = ""
        for c in range(colunas):
            valor = M[l, c]
            if isinstance(valor, complex):
                if decimais is None:
                    string_valor = f"\\complexnum{{{valor}}}"
                else:
                    string_valor = f"\\complexnum{{{valor:.{decimais}f}}}"
            else:
                if decimais is None:
                    string_valor = f"\\num{{{valor}}}"
                else:
                    string_valor = f"\\num{{{valor:.{decimais}f}}}"
            string_linha += f"{string_valor}"
            if c < colunas - 1:
                string_linha += " & "
        string_linha += " \\\\\n" if l < linhas - 1 else "\n"
        string_matrix += string_linha

    string_matrix += "\\end{bmatrix}\n\\end{equation}"
    print(string_matrix)


if __name__ == "__main__":
    M = sist.Observador.LQR.P.Polos
    matriz2latex(
        M,
    )
