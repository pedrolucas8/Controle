import control as ct
import control.matlab as cmat
import matplotlib.pyplot as plt
import numpy as np


def graficos(resultado):
    FONTESIZE_TITULO = 14
    FONTESIZE_LABEL = 12
    FONTESIZE_LEGENDA = 10
    LINEWIDTH = 1.5
    MARKERSIZE = 15
    B2 = resultado["B2"]
    C = resultado["C"]
    D = resultado["D"]
    # Polos_LQR = resultado.Controlador.LQR.Polos
    # Ganho_LQR = resultado.Controlador.LQR.Ganho

    sys_malha_aberta = resultado["sys_malha_aberta"]

    t = np.arange(start=0, stop=15, step=0.01)
    sys_mf1 = resultado["Controlador"]["Alocacao"]["P1"]["sys_mf"]
    # F1 = resultado.Controlador.Alocacao.P1.F
    # sys_mf1 = ss(F1, B2, C, D)
    # T, yout = ct.step_response(sys=sys_mf1, T=t)
    yout, T = cmat.step(sys=sys_mf1, T=t, input=0)
    yout2, T = cmat.step(sys=sys_mf1, T=t, input=1)
    print(sys_mf1)
    print(np.shape(T), np.shape(yout), np.shape(yout2))
    # print(yout[0][0])
    # ==========
    # fig = figure()
    # polos = pole(sys_malha_aberta)
    # zeros = zero(sys_malha_aberta)
    # hold on
    # plot(real(polos), imag(polos), 'kx','MarkerSize', MARKERSIZE, 'color', 'red', 'LineWidth', LINEWIDTH)
    # plot(real(zeros), imag(zeros), 'bo','MarkerSize', MARKERSIZE, 'color', 'blue', 'LineWidth', LINEWIDTH)
    # xlabel('Eixo Real', 'FontSize', FONTESIZE_LABEL)
    # ylabel('Eixo Imaginário', 'FontSize', FONTESIZE_LABEL)
    # legend('Polos', 'Zeros', 'FontSize', FONTESIZE_LEGENDA)
    # title('Polos e Zeros do Sistema', 'FontSize', FONTESIZE_TITULO)
    # grid on
    # xlim([-6 0.5])
    # set(gcf, 'PaperPositionMode', 'auto') # Ajusta o tamanho do papel para a tela cheia
    # saveas(fig, 'imagens/png/Polos_Zeros_Sistema', 'png')
    # saveas(fig, 'imagens/fig/Polos_Zeros_Sistema', 'fig')

    # figure()
    # plot(t_1, x_1(:,1,1), 'LineWidth', 1.5)
    # hold on
    # plot(t_1, x_1(:,2,1), 'LineWidth', 1.5)
    # plot(t_1, x_1(:,3,1), 'LineWidth', 1.5)
    # plot(t_1, x_1(:,4,1), 'LineWidth', 1.5)
    # grid on
    # xlabel('Tempo','Fontsize', 14)
    # ylabel('Variáveis de Estado','Fontsize', 14)
    # title('Evolução das Variáveis de Estado para a entrada degrau')
    # # legend('P2', 'P3', 'P4')
    # legend('Vel. horizontal [m/s]', 'Vel. vertical [m/s]', 'Taxa de arfagem [rad/s]', 'Ângulo de atitude [rad]')
    plt.figure(figsize=(12, 8))
    plt.plot(T, yout[:, 0], label="1 - input 0")
    plt.plot(T, yout[:, 1], label="2 - input 0")
    plt.plot(T, yout2[:, 0], label="3 - input 1")
    plt.plot(T, yout2[:, 1], label="4 - input 1")
    plt.grid()
    plt.legend()
    plt.show()
