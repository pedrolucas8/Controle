def Struct(resultado, topico, subtopicos, valor):
    if topico not in resultado:
        resultado[topico] = {}

    # Converte subtopicos para uma lista se for uma string
    if isinstance(subtopicos, str):
        subtopicos = [subtopicos]

    subresultado = resultado[topico]

    # Itera sobre os sub-tópicos e cria a estrutura aninhada
    for subtopico in subtopicos[:-1]:
        subresultado = subresultado.setdefault(subtopico, {})

    # Atribui o valor ao último sub-tópico
    subresultado[subtopicos[-1]] = valor

    return resultado
