from ..bibliotecas import *
from ..structtype import structtype


def seguidor_variavel(A, B1, B2, C, D, K, Ar, Cb):

    """
    Sistema
        x' = A x + B1 xw + B2 u
        y  = C x + D  u
    Assumindo que a referência e os distúrbios possuem dinâmica
        xr' = Ar xr
        xw' = Aw xw
    Aqui assumiremos que x e xr possuem o mesmo tamanho,
    logo a dinâmica do erro é dada por
        e = x - xr
        e' = x' - xr'
        e' = A x + B2 u + B1 xw - Ar xr
        e' = A (e+xr) + B2 u + B1 xw - Ar xr
        e' = A e + B2 u + B1 xw + (A-Ar) xr
    Definimos as variáveis exógenas como
        xex = [[xw], [xr]]
        Fex = [[B1, (A-Ar)]]
        A0 = [[Aw,0], [0,Ar]]
    A dinâmica do sistema fica
        e'   = A e + B2 u + Fex xex
        xex' = A0 xex
    E podemos definir a realimentação de controle como
        u = - K e - Kex xex
    Em regime permanente e'=0 e desejamos e->0
        e' = A e + B2 u + Fex xex
        e' = A e - B2 K e - B2 Kex xex + Fex xex
        0  = (A - B2 K) e + (Fex - B2 Kex) xex
        (A - B2 K) e = - (Fex - B2 Kex) xex
        e = - (A - B2 K)⁻¹ (Fex - B2 Kex) xex
    Vemos que não é possível manter o erro em zero, 
    visto que o sistema sofre atuação das variáveis externas xex
    Porém é possível anular uma combinação linear do erros
        z = Cb e
    Substituindo no sistema
        Cb e = - Cb (A - B2 K)⁻¹ (Fex - B2 Kex) xex = 0
    Para o caso não trivial xex!=0
        Cb (A - B2 K)⁻¹ (Fex - B2 Kex) = 0
        Cb (A - B2 K)⁻¹ B2 Kex = Cb (A - B2 K)⁻¹ Fex
    Que pode ser usada para calcular Kex
    Voltando para a dinâmica original
        x' = A x + B1 xw + B2 u
        x' = A x + B1 xw - B2 K e - B2 Kex xex
        x' = A x + B1 xw - B2 K (x-xr) - B2 Kex xex
        x' = (A - B2 K) x + [[B1, B2 K]] [[xw],[xr]] - B2 Kex xex
        x' = (A - B2 K) x + ([[B1, B2 K]] - B2 Kex) xex
        x' = F x + Bex xex
    Para as variáveis de saída
        y = C x - D u
        y = C x - D K (x-xr) - D Kex xex
        y = (C - D K) x + [[0, D K]] [[xw],[xr]] - D Kex xex
        y = (C - D K) x + ([[0, D K]] - D Kex) xex
        y = Cr x + Dex xex
    Resumindo
        x'   = F x + Bex xex
        y    = Cr x + Dex xex
        xex' = A0 xex
    """



    F = A - B2@K
    Fex = np.hstack(( B1 , A-Ar ))

    """
    Calculando Kex
        Cb (A - B2 K)⁻¹ B2 Kex = Cb (A - B2 K)⁻¹ Fex
        N = Cb (A - B2 K)⁻¹
        N (A - B2 K) = Cb
        (A - B2 K)^T N^T = Cb^T
        (N B2) Kex = (N Fex)
    """
    N = np.linalg.solve(F.transpose(),Cb.transpose())
    N = N.transpose()

    # Kex = np.linalg.solve(N@B2,N@Fex)
    Kex = np.linalg.lstsq(N@B2,N@Fex,None)[0]

    Bex = np.hstack(( B1 , B2@K )) - B2@Kex

    Cr = C - D@K

    # nx = A.shape[1]
    nw = B1.shape[1]
    # nu = B2.shape[1]
    ny = C.shape[0]
    Dex = np.hstack(( np.zeros((ny,nw)), D@K )) - D@Kex

    sys_mf1 = ct.ss(F, Bex, Cr, Dex)

    Seguidor = structtype(
        Ganhos = K,
        F = F,
        Kex = Kex,
        N = N,
        sys_mf=sys_mf1,
    )
    return Seguidor
