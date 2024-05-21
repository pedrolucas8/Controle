# Repositório remoto para o trabalho de controle
O projeto foi implementado usando `Python (v3.10)`.

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
## Uso do “*struct"*

Suponha que você queira salvar algum dado no struct principal do projeto, o struct *resultado*. Como fazer isso? E depois de salvo, como usar esse valor posteriormente?

Segue um exemplo de uso onde é feito um cálculo da soma de 2 números e usa o *struct* para salvar os valores usados na soma e o resultado.

```python
from main import sist

sist.Show()
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
