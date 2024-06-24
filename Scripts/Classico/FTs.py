# importando as bibliotecas necessárias
from Controle import *
from Scripts import *

# Definicao do sistema #
sist = get_sistema()

A = sist.sistema.A
# B1 = sist.sistema.B1
B2 = sist.sistema.B2
C = sist.sistema.C
D = sist.sistema.D
sys_ss = ct.ss(A,B2,C,D)
sys_tf = ct.ss2tf(sys_ss)

