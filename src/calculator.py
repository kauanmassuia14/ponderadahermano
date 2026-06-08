"""
Módulo de calculadora científica.

Fornece operações matemáticas básicas e avançadas com
validação de entrada e tratamento de erros apropriado.
"""

import math
from typing import List, Union

Number = Union[int, float]


def soma(a: Number, b: Number) -> Number:
    """Retorna a soma de dois números."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Os argumentos devem ser numéricos")
    return a + b


def subtracao(a: Number, b: Number) -> Number:
    """Retorna a subtração de dois números."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Os argumentos devem ser numéricos")
    return a - b


def multiplicacao(a: Number, b: Number) -> Number:
    """Retorna a multiplicação de dois números."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Os argumentos devem ser numéricos")
    return a * b


def divisao(a: Number, b: Number) -> float:
    """Retorna a divisão de dois números.

    Raises:
        ZeroDivisionError: Se o divisor for zero.
        TypeError: Se os argumentos não forem numéricos.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Os argumentos devem ser numéricos")
    if b == 0:
        raise ZeroDivisionError("Divisão por zero não é permitida")
    return a / b


def potencia(base: Number, expoente: Number) -> Number:
    """Retorna a base elevada ao expoente."""
    if not isinstance(base, (int, float)) or not isinstance(expoente, (int, float)):
        raise TypeError("Os argumentos devem ser numéricos")
    return base ** expoente


def raiz_quadrada(n: Number) -> float:
    """Retorna a raiz quadrada de um número.

    Raises:
        ValueError: Se o número for negativo.
    """
    if not isinstance(n, (int, float)):
        raise TypeError("O argumento deve ser numérico")
    if n < 0:
        raise ValueError("Não é possível calcular raiz quadrada de número negativo")
    return math.sqrt(n)


def fatorial(n: int) -> int:
    """Retorna o fatorial de um número inteiro não-negativo.

    Raises:
        ValueError: Se o número for negativo.
        TypeError: Se o número não for inteiro.
    """
    if not isinstance(n, int):
        raise TypeError("O argumento deve ser um inteiro")
    if n < 0:
        raise ValueError("Fatorial não é definido para números negativos")
    return math.factorial(n)


def media(numeros: List[Number]) -> float:
    """Retorna a média aritmética de uma lista de números.

    Raises:
        ValueError: Se a lista estiver vazia.
    """
    if not numeros:
        raise ValueError("A lista não pode estar vazia")
    if not all(isinstance(n, (int, float)) for n in numeros):
        raise TypeError("Todos os elementos devem ser numéricos")
    return sum(numeros) / len(numeros)


def mediana(numeros: List[Number]) -> float:
    """Retorna a mediana de uma lista de números.

    Raises:
        ValueError: Se a lista estiver vazia.
    """
    if not numeros:
        raise ValueError("A lista não pode estar vazia")
    if not all(isinstance(n, (int, float)) for n in numeros):
        raise TypeError("Todos os elementos devem ser numéricos")
    ordenados = sorted(numeros)
    n = len(ordenados)
    meio = n // 2
    if n % 2 == 0:
        return (ordenados[meio - 1] + ordenados[meio]) / 2
    return float(ordenados[meio])


def desvio_padrao(numeros: List[Number]) -> float:
    """Retorna o desvio padrão de uma lista de números.

    Raises:
        ValueError: Se a lista tiver menos de 2 elementos.
    """
    if len(numeros) < 2:
        raise ValueError("A lista deve ter pelo menos 2 elementos")
    if not all(isinstance(n, (int, float)) for n in numeros):
        raise TypeError("Todos os elementos devem ser numéricos")
    m = media(numeros)
    variancia = sum((x - m) ** 2 for x in numeros) / (len(numeros) - 1)
    return math.sqrt(variancia)
