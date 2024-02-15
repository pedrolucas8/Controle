# Repositório remoto para o trabalho de controle
O projeto foi feito baseado no trabalho feito em Matlab, ou seja, todas as funções presentes naquele projeto foram implementadas usando `Python (v3.11.6)`.

A biblioteca principal é `control (v0.9.4)`, ela é uma biblioteca dedicada ao desenvolvimento de sistemas de controle e possui algumas funções compatíveis com as do Matlab. A documentação dessa biblioteca pode ser encontrada na seção de referências. Outras bibliotecas que estão sendo usadas no projeto são: `numpy (v1.26.1)` para computação numérica, `scipy (v1.11.3)` é uma extensão que fornece ferramentas adicionais para análise e processamento científico e `matplotlib (v3.8.0)` para a criação de gráficos.

## Iniciando o projeto

Clone o projeto (ao conseguir acessar o projeto clique no botão verde escrito Code e copie a url)

```bash
git clone <https://link-para-o-projeto>
```

Entre no diretório do projeto

```bash
cd my-project
```

Instale as dependências (observação: )

```bash
pip install pacotes.txt
```

Rode o programa

```bash
python main.py
```

## Estrutura de pastas

O projeto está separado em pequenos pacotes.

A organização do projeto segue as diretrizes impostas do trabalho de controle, sendo assim, a organização final dos componentes principais é:

- `main.py` - arquivo principal, a partir dele as outras funções são chamadas.
- `graficos.py` - arquivo que gera todos os gráficos necessários para o relatório e apresentação.
- `bibliotecas.py` - arquivo que contém todos os módulos já importados para utilizar.
- `struct_dict.py` - arquivo responsável por gerar um dicionário em Python “parecido” com o `struct` do Matlab.
- `pacotes.txt` - arquivo de texto que contém todas as bibliotecas e suas respectivas versões que estão sendo usadas no projeto.
- `ControleModerno` - pacote que contém todas as funções relacionadas ao controle moderno, e.g. alocação de polos, LQR, etc.
- `ControleClassico` - pacote que contém todas as funções relacionadas ao controle clássico, e.g. Zigler-Nichols, PID, etc.
- `Imagens` - pasta onde todas as imagens são salvas
    - `PNG` - pasta onde os arquivos de imagem `.png` são salvos.
    - `JPEG` - pasta onde os arquivos de imagem `.jpeg` são salvos.

```bash
Controle/
│
├── main.py
├── graficos.py
├── bibliotecas.py
├── struct_dict.py
├── pacotes.txt
├── .gitignore
├── README.md
│
├── ControleModerno/
│   ├── __init__.py
│   ├── estabilidade.py
│   ├── controlabilidade.py
│   ├── observabilidade.py
│   └── ...
│
├── ControleClassico/
│   ├── __init__.py
│   ├── funcao1_classico.py
│   ├── funcao2_classico.py
│   └── ...
│
└── Imagens/
    ├── PNG/
    │   └── ...
    └── JPEG/
        └── ...
```

## Uso do “*struct"*

Suponha que você queira salvar algum dado no struct principal do projeto, o struct *resultado*. Como fazer isso? E depois de salvo, como usar esse valor posteriormente?

Segue um exemplo de uso onde é feito um cálculo da soma de 2 números e usa o *struct* para salvar os valores usados na soma e o resultado.

```python
# importanto todas as funções do arquivo struct_dict
from struct_dict import *

def soma(resultado, a, b):
	# salvando os dados que eu quero no struct
	resultado = Struct(resultado, "Soma", "Valor1", a)
	resultado = Struct(resultado, "Soma", "Valor2", b)
	resultado = Struct(resultado, "Soma", "Resultado", a + b)
	return resultado

# inicializando o dicionário (esse comando no projeto fica na main.py)
resultado = dict()

resultado = soma(resultado, 2, 3)

# acessando os dados através do dicionário
valor_1 = resultado["Soma"]["Valor1"] # acessando o valor salvo nessa variável (a = 2)
valor_1 = resultado["Soma"]["Valor2"] # acessando o valor salvo nessa variável (b = 3)
resultado_soma = resultado["Soma"]["Resultado"] # acessando o resultado salvo (5)
```

Observação: caso o seu dado esteja dentro de um contexto você pode criar uma lista. Por exemplo, você está fazendo a síntese do controlador por alocação de polos e você deseja salvar os polos usados e a matriz de ganho, você pode salvar desta maneira:

```python
# salvando os dados que eu quero no struct
resultado = Struct(resultado, "Controlador", ["Alocacao", "P", "Polos"], P)
resultado = Struct(resultado, "Controlador", ["Alocacao", "P", "Ganhos"], K)

# acessando os dados através do dicionário
Polos = resultado["Controlador"]["Alocacao"]["P"]["Polos"]
Matriz_Ganhos = resultado["Controlador"]["Alocacao"]["P"]["Ganhos"]
```

## Referência para as bibliotecas

- [Documentação da Biblioteca Control](https://python-control.readthedocs.io/en/0.9.4/)
- [Documentação da Biblioteca Numpy](https://numpy.org/doc/stable/index.html)
- [Documentação da Biblioteca Scipy](https://docs.scipy.org/doc/scipy/)
- [Documentação da Biblioteca Matplotlib](https://matplotlib.org/stable/index.html)

## Referência para sistemas de controle

- [Post - Understanding Bode plots](https://www.rohde-schwarz.com/us/products/test-and-measurement/essentials-test-equipment/digital-oscilloscopes/understanding-bode-plots_254514.html)
- [Playlist - Control System](https://youtube.com/playlist?list=PLBlnK6fEyqRhqzJT87LsdQKYZBC93ezDo&si=Bji73GUWSX1VII5g)
- [Playlist - All Control System Lecture Videos](https://youtube.com/playlist?list=PLUMWjy5jgHK3j74Z5Tq6Tso1fSfVWZC8L&si=DntNp8lRTW5gCvOn)
- [Playlist - Flight Mechanics](https://youtube.com/playlist?list=PLxdnSsBqCrrEx3A6W94sQGClk6Q4YCg-h&si=YxM-bFNkkXNMnLCy)
- [Playlist - Classical Control Theory](https://youtube.com/playlist?list=PLUMWjy5jgHK1NC52DXXrriwihVrYZKqjk&si=uqYKNm6evKRc5Ws8)
- [Livro - Control System Design Friedland](https://www.polishare.com.br/file.php?id=mLgz)
- [Apostila do Fleury](https://www.polishare.com.br/file.php?id=yak7)
- [Curso MIT - Systems And Controls](https://ocw.mit.edu/courses/2-04a-systems-and-controls-spring-2013/pages/lecture-notes-labs/)
