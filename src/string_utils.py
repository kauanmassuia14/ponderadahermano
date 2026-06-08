"""
Módulo de utilitários para manipulação de strings.

Fornece funções auxiliares para operações comuns com texto,
como inversão, contagem, verificação de palíndromos e formatação.
"""

from typing import List


def reverter(texto: str) -> str:
    """Retorna o texto invertido.

    Raises:
        TypeError: Se o argumento não for uma string.
    """
    if not isinstance(texto, str):
        raise TypeError("O argumento deve ser uma string")
    return texto[::-1]


def contar_vogais(texto: str) -> int:
    """Retorna a quantidade de vogais no texto.

    Considera vogais com e sem acentuação.
    """
    if not isinstance(texto, str):
        raise TypeError("O argumento deve ser uma string")
    vogais = set("aeiouáéíóúâêîôûãõAEIOUÁÉÍÓÚÂÊÎÔÛÃÕ")
    return sum(1 for char in texto if char in vogais)


def eh_palindromo(texto: str) -> bool:
    """Verifica se o texto é um palíndromo.

    Ignora espaços e diferenças entre maiúsculas/minúsculas.
    """
    if not isinstance(texto, str):
        raise TypeError("O argumento deve ser uma string")
    limpo = texto.replace(" ", "").lower()
    return limpo == limpo[::-1]


def capitalizar_palavras(texto: str) -> str:
    """Capitaliza a primeira letra de cada palavra."""
    if not isinstance(texto, str):
        raise TypeError("O argumento deve ser uma string")
    return texto.title()


def remover_duplicatas(texto: str) -> str:
    """Remove caracteres duplicados mantendo a ordem original."""
    if not isinstance(texto, str):
        raise TypeError("O argumento deve ser uma string")
    vistos = set()
    resultado = []
    for char in texto:
        if char not in vistos:
            vistos.add(char)
            resultado.append(char)
    return "".join(resultado)


def contar_palavras(texto: str) -> int:
    """Retorna a quantidade de palavras no texto."""
    if not isinstance(texto, str):
        raise TypeError("O argumento deve ser uma string")
    return len(texto.split())


def truncar(texto: str, max_len: int, sufixo: str = "...") -> str:
    """Trunca o texto no comprimento máximo, adicionando sufixo.

    Se o texto for menor ou igual ao max_len, retorna sem alteração.
    """
    if not isinstance(texto, str):
        raise TypeError("O argumento deve ser uma string")
    if max_len < 0:
        raise ValueError("O comprimento máximo deve ser não-negativo")
    if len(texto) <= max_len:
        return texto
    return texto[:max_len - len(sufixo)] + sufixo


def extrair_numeros(texto: str) -> List[int]:
    """Extrai todos os números inteiros de uma string."""
    if not isinstance(texto, str):
        raise TypeError("O argumento deve ser uma string")
    resultado = []
    numero_atual = ""
    for char in texto:
        if char.isdigit():
            numero_atual += char
        else:
            if numero_atual:
                resultado.append(int(numero_atual))
                numero_atual = ""
    if numero_atual:
        resultado.append(int(numero_atual))
    return resultado
