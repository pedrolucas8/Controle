import numpy as np
from scipy.optimize import root
from .structtype import structtype


def parametros_numericos():
    # Constantes
    rho = 1.225
    g = 9.81
    Uref = 4

    # Geométricos
    m = 12.3
    Iy = 0.550
    z_motor = 0.190
    S = 1.25
    mac = 0.51
    lambda_ = 0
    x1 = -0.027
    x2 = 1.130
    xCG = 0.154
    xAC1 = xCG + x1
    xAC2 = xCG + x2
    AR1 = 4
    AR2 = 5.92

    # Aerodinamicos
    dtau_dV = -0.917
    CL0 = 0.82
    CD0 = 0.0860
    CM0 = 0.0023
    CL_alpha = 3.80
    CD_alpha = 0.533
    CM_alpha = -0.559
    CL_eta = 0.47
    CD_eta = 0.015
    CM_eta = -1.011
    cl_alpha1 = 6.24
    cl_alpha2 = 6.25
    CL1_alpha = 3.47
    CL2_alpha = 0.33
    CD1_alpha = 0.529
    CD2_alpha = 0.004

    # ==============================
    # ========== TRIMAGEM ==========
    # ==============================
    # Velocidade Inicial
    V0 = 16.0

    # Chute Inicial
    x0 = np.array([[0.0], [0.0], [10]])
    q = 0.5 * rho * V0**2 * S

    # Equações do Movimento
    def fun(x):
        CL0 = 0.0  # Defina os valores de CL0, CD0, CM0, CL_alpha, CL_eta, CD_alpha, CD_eta, CM_alpha, CM_eta
        CD0 = 0.0
        CM0 = 0.0
        CL_alpha = 0.0
        CL_eta = 0.0
        CD_alpha = 0.0
        CD_eta = 0.0
        CM_alpha = 0.0
        CM_eta = 0.0

        return [
            q * (CL0 + CL_alpha * x[0] + CL_eta * x[1]) * np.sin(x[0])
            + x[2]
            - q * (CD0 + CD_alpha * x[0] + CD_eta * x[1]) * np.cos(x[0])
            - m * g * np.sin(x[0]),
            m * g * np.cos(x[0])
            - q * (CL0 + CL_alpha * x[0] + CL_eta * x[1]) * np.cos(x[0])
            - q * (CD0 + CD_alpha * x[0] + CD_eta * x[1]) * np.sin(x[0]),
            q * mac * (CM0 + CM_alpha * x[0] + CM_eta * x[1]) + z_motor * x[2],
        ]

    # Variáveis Trimadas

    # Método para resolver mínimos quadrados: Levenberg-Marquardt
    # Segundo essa resposta do stackoverflow, esse é o mesmo método que o fsolve do Matlab utiliza.
    # Url: https://stackoverflow.com/questions/21885093/comparing-fsolve-results-in-python-and-matlab
    y = root(fun, x0, method="lm")

    alpha_e = y.x[0]
    eta_e = y.x[1]
    tau_e = y.x[2]
    Ue = V0 * np.cos(alpha_e)
    We = V0 * np.sin(alpha_e)

    # ======================================
    # DERIVADAS DE ESTABILIDADE DIMENSIONAIS
    # ======================================
    CL = CL0 + CL_alpha * alpha_e + CL_eta * eta_e
    CD = CD0 + CD_alpha * alpha_e + CD_eta * eta_e

    # Gravitacionais
    Xg = -m * g * np.cos(alpha_e)
    Zg = -m * g * np.sin(alpha_e)

    # Potencia
    Xt = 1
    Zt = 0
    Mt = z_motor

    # Aerodinamicas
    Xu = -rho * V0 * S * CD + dtau_dV
    Zu = -rho * V0 * S * CL
    Mu = 0
    Xw = 0.5 * rho * V0 * S * (CL - CD_alpha)
    Zw = 0.5 * rho * V0 * S * (-CD - CL_alpha)
    Mw = 0.5 * rho * V0 * S * mac * CM_alpha
    Xq = -0.5 * rho * V0 * S * (xAC1 * CD1_alpha + xAC2 * CD2_alpha)
    Zq = (
        -0.25
        * rho
        * V0
        * S
        * mac
        * ((0.5 + 2 * x1 / mac) * CL1_alpha + (0.5 + 2 * x2 / mac) * CL2_alpha)
    )
    cmq1 = (
        -0.7
        * cl_alpha1
        * np.cos(np.radians(lambda_))
        * (
            (AR1 * (2 * (x1 / mac) ** 2 + 0.5 * (x1 / mac)))
            / (AR1 + 2 * np.cos(np.radians(lambda_)))
            + (
                AR1**3
                * np.tan(np.radians(lambda_)) ** 2
                / (AR1 + 6 * np.cos(np.radians(lambda_)))
            )
            / 24
            + 1 / 8
        )
    )
    cmq2 = (
        -0.7
        * cl_alpha2
        * np.cos(np.radians(lambda_))
        * (
            (AR2 * (2 * (x2 / mac) ** 2 + 0.5 * (x2 / mac)))
            / (AR2 + 2 * np.cos(np.radians(lambda_)))
            + (
                AR2**3
                * np.tan(np.radians(lambda_)) ** 2
                / (AR2 + 6 * np.cos(np.radians(lambda_)))
            )
            / 24
            + 1 / 8
        )
    )
    Mq = 0.25 * rho * V0 * S * mac**2 * (cmq1 + cmq2)

    # Controle
    Xn = -0.5 * rho * V0**2 * S * CD_eta
    Zn = -0.5 * rho * V0**2 * S * CL_eta
    Mn = 0.5 * rho * V0**2 * S * mac * CM_eta

    # ======================================
    # ========== MUDANÇA DE EIXOS ==========
    # ======================================
    # Variáveis Auxiliares
    aux1 = np.cos(alpha_e)
    aux2 = np.sin(alpha_e)
    aux3 = aux1**2
    aux4 = aux2**2
    # Eixo do Vento --> Eixo do Corpo
    Xu = Xu * aux3 + Zw * aux4 - (Xw + Zu) * aux1 * aux2
    Xw = Xw * aux3 - Zu * aux4 + (Xu - Zw) * aux1 * aux2
    Zu = Zu * aux3 - Xw * aux4 + (Xu - Zw) * aux1 * aux2
    Zw = Zw * aux3 + Xu * aux4 + (Xw + Zu) * aux1 * aux2
    Mu = Mu * aux1 - Mw * aux2
    Mw = Mw * aux1 + Mu * aux2
    Xq = Xq * aux1 - Zq * aux2
    Zq = Zq * aux1 + Xq * aux2
    Xn = Xn * aux1 - Zn * aux2
    Zn = Zn * aux1 + Xn * aux2

    A = np.matrix(
        [
            [Xu / m, Xw / m, Xq / m - We, Xg / m],
            [Zu / m, Zw / m, Zq / m + Ue, Zg / m],
            [Mu / Iy, Mw / Iy, Mq / Iy, 0],
            [0, 0, 1, 0],
        ]
    )

    B = np.matrix(
        [
            [Xn / m, Xt / m],
            [Zn / m, 0],
            [Mn / Iy, Mt / Iy],
            [0, 0],
        ]
    )
    # print(A)
    # print()
    # print(B)
    return A, B


def def_sistema(sist):
    # Matriz de estados. x = [u, w, q, theta]'
    # A, B = parametros_numericos()
    A = np.matrix(
        [
            [-0.2655, -0.1235, 0.8388, -9.7925],
            [-1.4412, -3.7332, 15.2192, 0.5863],
            [-0.3795, -6.3157, -4.7475, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ]
    )

    # # Matriz de entrada de disturbios
    # B1 = np.matrix(([-0.1235, 0.0], [-3.7332, -1.0], [-6.3157, 0.0], [0.0, 0.0]))
    B1 = A[:,:2]

    # Matriz de entradas de controle
    B2 = np.matrix([[-0.6862, 0.0813], [-7.4350, 0.0], [-183.7447, 0.3455], [0.0, 0.0]])
    # B2 = B

    # Matriz de observacao y = [u, w]'
    C = np.matrix([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0]
    ])

    # Matriz de alimentação direta
    D = np.zeros((np.shape(C)[0], np.shape(B2)[1]))

    # Nome das variáveis
    estados = [
        "Vel Horizontal (u) [m/s]",
        "Vel Vertical (w) [m/s]",
        "Taxa Arfagem (q) [rad/s]",
        "Ang Atitude (θ) [rad]",
    ]
    controle = [
        "Def Profundor (η) [rad]", 
        "Tração (τ) [N]",
    ]
    perturbacoes = [
        "Vel vertical (Ugust) [m/s]",
        "Acel vertical (U'gust) [m/s]",
    ]
    saidas = [
        "Vel Horizontal (u) [m/s]",
        "Vel Vertical (w) [m/s]",
    ]

    # Salva o resultado
    sist.sistema = structtype(
        A=A,
        B1=B1,
        B2=B2,
        C=C,
        D=D,
        estados=estados,
        controle=controle,
        perturbacoes=perturbacoes,
        saidas=saidas,
    )
