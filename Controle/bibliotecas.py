# Adiciona o diretório 'Controle' ao sys.path
import sys
import os

diretorio_atual = os.path.dirname(__file__)
diretorio_pai = os.path.abspath(os.path.join(diretorio_atual, ".."))

diretorio_controle = os.path.abspath(os.path.join(diretorio_pai, "Controle"))
print(f"Adicionando {diretorio_controle} ao sys.path")
if diretorio_controle not in sys.path:
    sys.path.append(diretorio_controle)

diretorio_scripts = os.path.abspath(os.path.join(diretorio_pai, "Scripts"))
print(f"Adicionando {diretorio_scripts} ao sys.path")
if diretorio_scripts not in sys.path:
    sys.path.append(diretorio_scripts)

# Matemática
import numpy as np
import math
import scipy

# Controle
import control as ct
import control.matlab as cmat

# Outros
import sys, os
import json

# Plots
# import matplotlib.pyplot as plt
import plotly