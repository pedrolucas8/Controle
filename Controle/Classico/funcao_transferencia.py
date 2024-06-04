from ..bibliotecas import *
from ..structtype import structtype


def funcao_transferencia():
    """Funções de transferência do sistema.
    FT1: (eta) -> (u) -> índice 0
    FT2: (eta) -> (w) -> índice 1
    FT1: (tau) -> (u) -> índice 2
    FT2: (tau) -> (w) -> índice 3
    """

    # FTs obtidas via MATLAB
    # From input "Def. Profundor (eta)" to output "Vel. Horizontal (u)"
    TF1_num = np.array([-0.6862, -159, 1535, +6268])
    # From input "Def. Profundor (eta)" to output "Vel. Vertical (w)"
    TF2_num = np.array([-7.435, -2833, -631.1, -2594])
    # From input "Tração (tau)" to output "Vel. Horizontal (u)"
    TF3_num = np.array([0.0813, 0.9793, 6.305, -12.35])
    # From input "Tração (tau)" to output "Vel. Vertical (w)"
    TF4_num = np.array([5.141, 0.1551, 4.912])
    # O denominador das funcões de transferência é o mesmo
    TF_den = np.array([1, 8.746, 116.2, 22.21, 76.22])

    # Criando as funções de transferência
    TF1 = ct.TransferFunction(TF1_num, TF_den)
    TF2 = ct.TransferFunction(TF2_num, TF_den)
    TF3 = ct.TransferFunction(TF3_num, TF_den)
    TF4 = ct.TransferFunction(TF4_num, TF_den)

    TFs = structtype(TF1=TF1, TF2=TF2, TF3=TF3, TF4=TF4)

    return TFs


if __name__ == "__main__":

    A = np.array(
        [
            [-0.2655, -0.1235, 0.8388, -9.7925],
            [-1.4412, -3.7332, 15.2192, 0.5863],
            [-0.3795, -6.3157, -4.7475, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ]
    )
    B = np.array(
        [
            [-6.862000e-01, 8.130000e-02],
            [-7.435000e00, 0.000000e00],
            [-1.837447e02, 3.455000e-01],
            [0.000000e00, 0.000000e00],
        ]
    )
    C = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]])
    D = np.array([[0.0, 0.0], [0.0, 0.0]])

    TFs = funcao_transferencia(A, B, C, D)

    print(TFs)
