# importando as bibliotecas necessárias
from bibliotecas import *
from struct_dict import *


def controlador_alocacao_polos(resultado, A, B, C, D):
    # Alocação de polos para o controlador
    # Ref: Capitulo 10 do livro Flight Dynamics Principles (Cook)
    # [P1, K1] = alocacao_Cook(A, B);
    P1 = np.array([-0.5 + 2j, -0.5 - 2j, -30 + 5j, -30 - 5j])
    K1 = scipy.signal.place_poles(A, B, P1, method="YT", maxiter=30)
    K1 = K1.gain_matrix
    F1 = A - np.matmul(B, K1)
    sys_mf1 = ct.ss(F1, B, C, D)

    P2 = np.array([-0.5 + 4j, -0.5 - 4j, -25 - 1.5j, -25 + 1.5j])
    K2 = scipy.signal.place_poles(A, B, P2, method="YT", maxiter=30)
    K2 = K2.gain_matrix
    F2 = A - np.matmul(B, K2)
    sys_mf2 = ct.ss(F2, B, C, D)

    P3 = np.array([-0.5 + 1j, -0.5 - 1j, -4.5 + 6j, -4.5 - 6j])
    K3 = scipy.signal.place_poles(A, B, P3, method="YT", maxiter=30)
    K3 = K3.gain_matrix
    F3 = A - np.matmul(B, K3)
    sys_mf3 = ct.ss(F3, B, C, D)

    P4 = np.array([-0.1500 + 0.8133j, -0.1500 - 0.8133j, -25 + 1.9713j, -25 - 1.9713j])
    K4 = scipy.signal.place_poles(A, B, P4, method="YT", maxiter=30)
    K4 = K4.gain_matrix
    F4 = A - np.matmul(B, K4)
    sys_mf4 = ct.ss(F4, B, C, D)

    P5 = np.array([-2, -4, -3 + 6j, -3 - 6j])
    K5 = scipy.signal.place_poles(A, B, P5, method="YT", maxiter=30)
    K5 = K5.gain_matrix
    F5 = A - np.matmul(B, K5)
    sys_mf5 = ct.ss(F5, B, C, D)

    # # ==========
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P1", "Polos"], P1)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P1", "Ganhos"], K1)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P1", "F"], F1)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P1", "sys_mf"], sys_mf1)
    # ==========
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P2", "Polos"], P2)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P2", "Ganhos"], K2)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P2", "F"], F2)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P2", "sys_mf"], sys_mf2)
    # ==========
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P3", "Polos"], P3)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P3", "Ganhos"], K3)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P3", "F"], F3)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P3", "sys_mf"], sys_mf3)
    # ==========
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P4", "Polos"], P4)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P4", "Ganhos"], K4)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P4", "F"], F4)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P4", "sys_mf"], sys_mf4)
    # ==========
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P5", "Polos"], P5)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P5", "Ganhos"], K5)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P5", "F"], F5)
    resultado = Struct(resultado, "Controlador", ["Alocacao", "P5", "sys_mf"], sys_mf5)
    # ==========

    return resultado


if __name__ == "__main__":
    A = np.array(
        [
            [-0.2655, -0.1235, 0.8388, -9.7925],
            [-1.4412, -3.7332, 15.2192, 0.5863],
            [-0.3795, -6.3157, -4.7475, 0],
            [0, 0, 1, 0],
        ]
    )
    B2 = np.array([[-0.6862, 0.0813], [-7.4350, 0], [-183.7447, 0.3455], [0, 0]])
    (_, colunas_B2) = np.shape(B2)

    C = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
    (linhas_C, _) = np.shape(C)

    D = np.zeros((linhas_C, colunas_B2))

    resultado = dict()
    resultado = controlador_alocacao_polos(resultado, A, B2, C, D)
    print(resultado["Controlador"]["Alocacao"]["P2"]["Ganhos"])
