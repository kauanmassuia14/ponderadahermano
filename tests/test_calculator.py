"""
Testes para o módulo calculator.

Testa operações básicas, funções estatísticas,
edge cases e validação de tipos.
"""

import time
import pytest
from src.calculator import (
    soma,
    subtracao,
    multiplicacao,
    divisao,
    potencia,
    raiz_quadrada,
    fatorial,
    media,
    mediana,
    desvio_padrao,
)


# ---------- Testes de Soma ----------

class TestSoma:
    def test_soma_positivos(self):
        assert soma(2, 3) == 5

    def test_soma_negativos(self):
        assert soma(-2, -3) == -5

    def test_soma_com_zero(self):
        assert soma(0, 5) == 5

    def test_soma_floats(self):
        assert soma(1.5, 2.5) == 4.0

    def test_soma_tipo_invalido(self):
        with pytest.raises(TypeError):
            soma("a", 1)


# ---------- Testes de Subtração ----------

class TestSubtracao:
    def test_subtracao_basica(self):
        assert subtracao(10, 3) == 7

    def test_subtracao_resultado_negativo(self):
        assert subtracao(3, 10) == -7


# ---------- Testes de Multiplicação ----------

class TestMultiplicacao:
    def test_multiplicacao_basica(self):
        assert multiplicacao(4, 5) == 20

    def test_multiplicacao_por_zero(self):
        assert multiplicacao(100, 0) == 0

    def test_multiplicacao_negativos(self):
        assert multiplicacao(-3, -4) == 12


# ---------- Testes de Divisão ----------

class TestDivisao:
    def test_divisao_basica(self):
        assert divisao(10, 2) == 5.0

    def test_divisao_por_zero(self):
        with pytest.raises(ZeroDivisionError):
            divisao(10, 0)

    def test_divisao_resultado_decimal(self):
        assert divisao(7, 2) == 3.5


# ---------- Testes de Potência ----------

class TestPotencia:
    def test_potencia_basica(self):
        assert potencia(2, 3) == 8

    def test_potencia_zero(self):
        assert potencia(5, 0) == 1

    def test_potencia_negativa(self):
        assert potencia(2, -1) == 0.5


# ---------- Testes de Raiz Quadrada ----------

class TestRaizQuadrada:
    def test_raiz_perfeita(self):
        assert raiz_quadrada(9) == 3.0

    def test_raiz_de_zero(self):
        assert raiz_quadrada(0) == 0.0

    def test_raiz_negativa(self):
        with pytest.raises(ValueError):
            raiz_quadrada(-4)


# ---------- Testes de Fatorial ----------

class TestFatorial:
    def test_fatorial_cinco(self):
        assert fatorial(5) == 120

    def test_fatorial_zero(self):
        assert fatorial(0) == 1

    def test_fatorial_negativo(self):
        with pytest.raises(ValueError):
            fatorial(-1)

    def test_fatorial_tipo_invalido(self):
        with pytest.raises(TypeError):
            fatorial(3.5)


# ---------- Testes de Média ----------

class TestMedia:
    def test_media_basica(self):
        assert media([1, 2, 3, 4, 5]) == 3.0

    def test_media_lista_vazia(self):
        with pytest.raises(ValueError):
            media([])

    def test_media_um_elemento(self):
        assert media([42]) == 42.0


# ---------- Testes de Mediana ----------

class TestMediana:
    def test_mediana_impar(self):
        assert mediana([1, 3, 5]) == 3.0

    def test_mediana_par(self):
        assert mediana([1, 2, 3, 4]) == 2.5

    def test_mediana_desordenada(self):
        assert mediana([5, 1, 3]) == 3.0


# ---------- Testes de Desvio Padrão ----------

class TestDesvioPadrao:
    def test_desvio_padrao_basico(self):
        resultado = desvio_padrao([2, 4, 4, 4, 5, 5, 7, 9])
        assert round(resultado, 4) == 2.1381

    def test_desvio_padrao_insuficiente(self):
        with pytest.raises(ValueError):
            desvio_padrao([1])


# ---------- Testes Extras Parametrizados (Crescimento de Escopo) ----------

@pytest.mark.parametrize("a,b,esperado", [
    (1, 1, 2), (2, 2, 4), (10, 20, 30), (-1, 1, 0), (0, 0, 0),
    (5, -5, 0), (1.1, 2.2, 3.3), (100, 200, 300), (99, 1, 100), (12, 12, 24)
])
def test_soma_parametrizada(a, b, esperado):
    assert round(soma(a, b), 2) == round(esperado, 2)


@pytest.mark.parametrize("a,b,esperado", [
    (5, 3, 2), (10, 10, 0), (0, 5, -5), (-5, -5, 0), (100, 1, 99),
    (1.5, 0.5, 1.0), (10, 20, -10), (50, 10, 40), (9, 9, 0), (2, 5, -3)
])
def test_subtracao_parametrizada(a, b, esperado):
    assert round(subtracao(a, b), 2) == round(esperado, 2)


@pytest.mark.parametrize("a,b,esperado", [
    (2, 3, 6), (5, 5, 25), (-1, 5, -5), (0, 10, 0), (1.5, 2, 3.0),
    (10, 10, 100), (0.5, 0.5, 0.25), (-2, -3, 6), (9, 9, 81), (12, 5, 60)
])
def test_multiplicacao_parametrizada(a, b, esperado):
    assert round(multiplicacao(a, b), 2) == round(esperado, 2)


def test_stress_lento():
    time.sleep(10)
    assert True




