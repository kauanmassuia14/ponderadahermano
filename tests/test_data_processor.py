"""
Testes para o módulo data_processor.

Cobre filtragem, estatísticas, normalização,
detecção de outliers e operações de agrupamento.
"""

import pytest
from src.data_processor import (
    filtrar_pares,
    filtrar_impares,
    calcular_estatisticas,
    normalizar,
    detectar_outliers,
    agrupar_por_faixa,
    remover_valores_nulos,
    porcentagem_do_total,
)


# ---------- Testes de Filtrar Pares ----------

class TestFiltrarPares:
    def test_filtrar_pares(self):
        assert filtrar_pares([1, 2, 3, 4, 5, 6]) == [2, 4, 6]

    def test_filtrar_pares_vazio(self):
        assert filtrar_pares([]) == []

    def test_filtrar_pares_sem_pares(self):
        assert filtrar_pares([1, 3, 5]) == []


# ---------- Testes de Filtrar Ímpares ----------

class TestFiltrarImpares:
    def test_filtrar_impares(self):
        assert filtrar_impares([1, 2, 3, 4, 5]) == [1, 3, 5]

    def test_filtrar_impares_sem_impares(self):
        assert filtrar_impares([2, 4, 6]) == []


# ---------- Testes de Estatísticas ----------

class TestCalcularEstatisticas:
    def test_estatisticas_basicas(self):
        resultado = calcular_estatisticas([10, 20, 30])
        assert resultado["min"] == 10.0
        assert resultado["max"] == 30.0
        assert resultado["soma"] == 60.0
        assert resultado["media"] == 20.0
        assert resultado["contagem"] == 3.0

    def test_estatisticas_vazio(self):
        with pytest.raises(ValueError):
            calcular_estatisticas([])


# ---------- Testes de Normalizar ----------

class TestNormalizar:
    def test_normalizar_basico(self):
        resultado = normalizar([0, 50, 100])
        assert resultado == [0.0, 0.5, 1.0]

    def test_normalizar_valores_iguais(self):
        with pytest.raises(ValueError):
            normalizar([5, 5, 5])

    def test_normalizar_vazio(self):
        with pytest.raises(ValueError):
            normalizar([])


# ---------- Testes de Outliers ----------

class TestDetectarOutliers:
    def test_outlier_obvio(self):
        dados = [10, 12, 11, 13, 12, 11, 100]
        outliers = detectar_outliers(dados)
        assert 100 in outliers

    def test_sem_outliers(self):
        dados = [10, 11, 12, 13, 14]
        assert detectar_outliers(dados) == []

    def test_poucos_dados(self):
        with pytest.raises(ValueError):
            detectar_outliers([1, 2, 3])


# ---------- Testes de Agrupar por Faixa ----------

class TestAgruparPorFaixa:
    def test_agrupar_basico(self):
        resultado = agrupar_por_faixa(
            [1, 5, 10, 15, 20],
            [(1, 10), (11, 20)]
        )
        assert resultado["1-10"] == [1, 5, 10]
        assert resultado["11-20"] == [15, 20]


# ---------- Testes de Remover Nulos ----------

class TestRemoverNulos:
    def test_remover_nulos(self):
        assert remover_valores_nulos([1, None, 3, None, 5]) == [1, 3, 5]

    def test_sem_nulos(self):
        assert remover_valores_nulos([1, 2, 3]) == [1, 2, 3]


# ---------- Testes de Porcentagem ----------

class TestPorcentagemDoTotal:
    def test_porcentagem_basica(self):
        resultado = porcentagem_do_total([25, 25, 50])
        assert resultado == [25.0, 25.0, 50.0]

    def test_porcentagem_vazio(self):
        with pytest.raises(ValueError):
            porcentagem_do_total([])

    def test_porcentagem_soma_zero(self):
        with pytest.raises(ValueError):
            porcentagem_do_total([0, 0, 0])
