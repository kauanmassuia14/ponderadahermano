"""
Módulo de processamento de dados.

Fornece funções para filtragem, análise estatística,
normalização e detecção de anomalias em conjuntos de dados numéricos.
"""

from typing import Dict, List, Tuple, Union

Number = Union[int, float]


def filtrar_pares(numeros: List[int]) -> List[int]:
    """Retorna apenas os números pares da lista."""
    if not all(isinstance(n, int) for n in numeros):
        raise TypeError("Todos os elementos devem ser inteiros")
    return [n for n in numeros if n % 2 == 0]


def filtrar_impares(numeros: List[int]) -> List[int]:
    """Retorna apenas os números ímpares da lista."""
    if not all(isinstance(n, int) for n in numeros):
        raise TypeError("Todos os elementos devem ser inteiros")
    return [n for n in numeros if n % 2 != 0]


def calcular_estatisticas(numeros: List[Number]) -> Dict[str, float]:
    """Retorna um dicionário com estatísticas básicas.

    Chaves: min, max, soma, media, contagem

    Raises:
        ValueError: Se a lista estiver vazia.
    """
    if not numeros:
        raise ValueError("A lista não pode estar vazia")
    if not all(isinstance(n, (int, float)) for n in numeros):
        raise TypeError("Todos os elementos devem ser numéricos")
    return {
        "min": float(min(numeros)),
        "max": float(max(numeros)),
        "soma": float(sum(numeros)),
        "media": sum(numeros) / len(numeros),
        "contagem": float(len(numeros)),
    }


def normalizar(numeros: List[Number]) -> List[float]:
    """Normaliza os valores para o intervalo [0, 1] usando min-max.

    Raises:
        ValueError: Se a lista estiver vazia ou todos valores iguais.
    """
    if not numeros:
        raise ValueError("A lista não pode estar vazia")
    if not all(isinstance(n, (int, float)) for n in numeros):
        raise TypeError("Todos os elementos devem ser numéricos")
    min_val = min(numeros)
    max_val = max(numeros)
    if min_val == max_val:
        raise ValueError("Não é possível normalizar: todos os valores são iguais")
    return [(x - min_val) / (max_val - min_val) for x in numeros]


def detectar_outliers(numeros: List[Number], fator: float = 1.5) -> List[Number]:
    """Detecta outliers usando o método IQR (Interquartile Range).

    Args:
        numeros: Lista de números.
        fator: Multiplicador do IQR (padrão: 1.5).

    Returns:
        Lista de valores considerados outliers.
    """
    if len(numeros) < 4:
        raise ValueError("A lista deve ter pelo menos 4 elementos")
    if not all(isinstance(n, (int, float)) for n in numeros):
        raise TypeError("Todos os elementos devem ser numéricos")
    ordenados = sorted(numeros)
    n = len(ordenados)
    q1 = ordenados[n // 4]
    q3 = ordenados[3 * n // 4]
    iqr = q3 - q1
    limite_inferior = q1 - fator * iqr
    limite_superior = q3 + fator * iqr
    return [x for x in numeros if x < limite_inferior or x > limite_superior]


def agrupar_por_faixa(
    numeros: List[Number], faixas: List[Tuple[Number, Number]]
) -> Dict[str, List[Number]]:
    """Agrupa números em faixas especificadas.

    Args:
        numeros: Lista de números para agrupar.
        faixas: Lista de tuplas (inicio, fim) definindo cada faixa.

    Returns:
        Dicionário com chave no formato 'inicio-fim' e valores agrupados.
    """
    if not numeros:
        raise ValueError("A lista não pode estar vazia")
    resultado = {}
    for inicio, fim in faixas:
        chave = f"{inicio}-{fim}"
        resultado[chave] = [n for n in numeros if inicio <= n <= fim]
    return resultado


def remover_valores_nulos(dados: List) -> List:
    """Remove valores None de uma lista."""
    return [x for x in dados if x is not None]


def porcentagem_do_total(numeros: List[Number]) -> List[float]:
    """Calcula a porcentagem de cada valor em relação ao total.

    Raises:
        ValueError: Se a lista estiver vazia ou a soma for zero.
    """
    if not numeros:
        raise ValueError("A lista não pode estar vazia")
    total = sum(numeros)
    if total == 0:
        raise ValueError("A soma dos valores não pode ser zero")
    return [round((x / total) * 100, 2) for x in numeros]
