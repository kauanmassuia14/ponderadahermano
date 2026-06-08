"""
Testes para o módulo string_utils.

Cobre todas as funções de manipulação de strings
incluindo edge cases e validação de tipos.
"""

import pytest
from src.string_utils import (
    reverter,
    contar_vogais,
    eh_palindromo,
    capitalizar_palavras,
    remover_duplicatas,
    contar_palavras,
    truncar,
    extrair_numeros,
)


# ---------- Testes de Reverter ----------

class TestReverter:
    def test_reverter_palavra(self):
        assert reverter("python") == "nohtyp"

    def test_reverter_vazio(self):
        assert reverter("") == ""

    def test_reverter_tipo_invalido(self):
        with pytest.raises(TypeError):
            reverter(123)


# ---------- Testes de Contar Vogais ----------

class TestContarVogais:
    def test_contar_vogais_basico(self):
        assert contar_vogais("hello") == 2

    def test_contar_vogais_acentuadas(self):
        assert contar_vogais("programação") == 5

    def test_contar_sem_vogais(self):
        assert contar_vogais("xyz") == 0


# ---------- Testes de Palíndromo ----------

class TestEhPalindromo:
    def test_palindromo_simples(self):
        assert eh_palindromo("arara") is True

    def test_nao_palindromo(self):
        assert eh_palindromo("python") is False

    def test_palindromo_com_espacos(self):
        assert eh_palindromo("a man a") is False

    def test_palindromo_maiusculas(self):
        assert eh_palindromo("Aba") is True


# ---------- Testes de Capitalizar ----------

class TestCapitalizarPalavras:
    def test_capitalizar_basico(self):
        assert capitalizar_palavras("hello world") == "Hello World"

    def test_capitalizar_ja_capitalizado(self):
        assert capitalizar_palavras("Hello") == "Hello"


# ---------- Testes de Remover Duplicatas ----------

class TestRemoverDuplicatas:
    def test_remover_duplicatas(self):
        assert remover_duplicatas("abracadabra") == "abrcd"

    def test_sem_duplicatas(self):
        assert remover_duplicatas("abc") == "abc"


# ---------- Testes de Contar Palavras ----------

class TestContarPalavras:
    def test_contar_palavras(self):
        assert contar_palavras("eu gosto de python") == 4

    def test_contar_uma_palavra(self):
        assert contar_palavras("python") == 1


# ---------- Testes de Truncar ----------

class TestTruncar:
    def test_truncar_longo(self):
        assert truncar("Hello World", 8) == "Hello..."

    def test_truncar_curto(self):
        assert truncar("Hi", 10) == "Hi"

    def test_truncar_max_negativo(self):
        with pytest.raises(ValueError):
            truncar("test", -1)


# ---------- Testes de Extrair Números ----------

class TestExtrairNumeros:
    def test_extrair_numeros(self):
        assert extrair_numeros("abc123def456") == [123, 456]

    def test_extrair_sem_numeros(self):
        assert extrair_numeros("hello") == []

    def test_extrair_so_numeros(self):
        assert extrair_numeros("42") == [42]
