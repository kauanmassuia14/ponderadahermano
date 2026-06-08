# 📊 Instrumentação e Análise de Pipeline CI/CD

Projeto de experimentação prática para medir e analisar o comportamento de um pipeline CI/CD no GitHub Actions, coletando métricas reais de execução, gerando gráficos e produzindo análise técnica sobre desempenho, estabilidade e gargalos do processo.

## 📋 Sumário

- [Descrição do Projeto](#descrição-do-projeto)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [O Pipeline CI/CD](#o-pipeline-cicd)
- [Como Reproduzir o Experimento](#como-reproduzir-o-experimento)
- [Scripts de Coleta e Visualização](#scripts-de-coleta-e-visualização)
- [Variações Realizadas](#variações-realizadas)
- [Resultados](#resultados)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)

## 📝 Descrição do Projeto

Este repositório contém um projeto Python com **três módulos** (calculadora científica, utilitários de string e processador de dados) e uma suíte de **testes automatizados** usando pytest. O objetivo principal é instrumentar o pipeline CI/CD para:

1. **Medir** tempos de execução de cada etapa
2. **Coletar** métricas estruturadas via GitHub API
3. **Visualizar** tendências e padrões através de gráficos
4. **Analisar** gargalos, estabilidade e oportunidades de otimização

## 🗂 Estrutura do Projeto

```
├── .github/workflows/
│   └── ci.yml                    # Pipeline GitHub Actions
├── src/
│   ├── calculator.py             # Calculadora científica
│   ├── string_utils.py           # Utilitários de string
│   └── data_processor.py         # Processador de dados
├── tests/
│   ├── test_calculator.py        # Testes da calculadora (~30 testes)
│   ├── test_string_utils.py      # Testes de string utils (~20 testes)
│   └── test_data_processor.py    # Testes do processador (~18 testes)
├── scripts/
│   ├── collect_metrics.py        # Coleta métricas via GitHub API
│   └── generate_charts.py        # Gera gráficos com matplotlib
├── metrics/
│   ├── pipeline_metrics.csv      # Dados coletados em CSV
│   └── pipeline_metrics.json     # Dados coletados em JSON
├── charts/                       # Gráficos gerados
├── requirements.txt              # Dependências de produção
├── requirements-dev.txt          # Dependências de desenvolvimento
├── setup.cfg                     # Configuração do flake8
├── RELATORIO.md                  # Relatório técnico completo
└── README.md                     # Este arquivo
```

## 🔄 O Pipeline CI/CD

O pipeline (`ci.yml`) é executado a cada push na branch `main` e contém:

| Etapa | Descrição |
|-------|-----------|
| **Checkout** | Clona o repositório |
| **Setup Python** | Configura Python 3.11 |
| **Cache** | Cache de dependências pip |
| **Install** | Instala dependências |
| **Lint** | Análise estática com flake8 |
| **Test** | Executa testes com pytest |
| **Upload Results** | Salva resultados como artefato |
| **Collect Metrics** | Coleta métricas da execução |
| **Upload Metrics** | Salva métricas como artefato |

## 🚀 Como Reproduzir o Experimento

### Pré-requisitos

- Python 3.9+
- Git
- Conta no GitHub com acesso a GitHub Actions
- Personal Access Token do GitHub (para coleta de métricas)

### 1. Clonar o repositório

```bash
git clone https://github.com/kauanmassuia14/ponderadahermano.git
cd ponderadahermano
```

### 2. Instalar dependências localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### 3. Rodar testes localmente

```bash
pytest tests/ -v
```

### 4. Verificar lint

```bash
flake8 src/ tests/
```

### 5. Fazer push e observar o pipeline

```bash
git add .
git commit -m "feat: descrição da alteração"
git push origin main
```

O pipeline executará automaticamente no GitHub Actions.

### 6. Coletar métricas (após as execuções)

```bash
export GITHUB_TOKEN="seu_personal_access_token"
python scripts/collect_metrics.py
```

### 7. Gerar gráficos

```bash
python scripts/generate_charts.py
```

Os gráficos serão salvos na pasta `charts/`.

## 📊 Scripts de Coleta e Visualização

### `scripts/collect_metrics.py`

Script que consulta a **API REST do GitHub** para extrair dados de todas as execuções do workflow, incluindo:
- Tempo total de cada workflow run
- Tempo de cada job e step
- Status (sucesso/falha)
- Informações do commit (SHA, mensagem, data)
- Estado do cache

Gera um arquivo CSV e JSON em `metrics/`.

### `scripts/generate_charts.py`

Script que lê o CSV de métricas e gera **6 gráficos**:

1. **Tempo total do pipeline por execução** - Barras coloridas por status
2. **Tempo por etapa** - Comparação install vs lint vs test
3. **Taxa de sucesso e falha** - Pizza + barras por execução
4. **Testes vs duração** - Scatter plot com linha de tendência
5. **Impacto do cache** - Comparação com/sem cache
6. **Timeline de execuções** - Série temporal

## 🔬 Variações Realizadas

| # | Variação | Objetivo |
|---|----------|----------|
| 1 | Baseline (todos testes passando) | Linha de base |
| 2 | Teste falhando propositalmente | Medir impacto de falha |
| 3 | Corrigir teste falhando | Retorno ao normal |
| 4 | +20 testes parametrizados | Escalar quantidade |
| 5 | Teste lento (sleep 10s) | Simular gargalo |
| 6 | Remover teste lento | Retorno ao normal |
| 7 | Desativar cache | Medir impacto do cache |
| 8 | Reativar cache | Comparar com/sem cache |
| 9 | Erro de lint (violação flake8) | Falha em etapa diferente |
| 10 | Corrigir erro de lint | Retorno ao normal |
| 11 | Jobs paralelos (lint + test) | Medir ganho de paralelismo |
| 12 | Voltar para sequencial | Comparar com paralelo |
| 13 | Stress test (40 testes + lento) | Carga máxima |
| 14 | Pipeline limpo otimizado | Estado final |

## 📈 Resultados

Os resultados detalhados, gráficos e análise completa estão disponíveis no [RELATÓRIO TÉCNICO](RELATORIO.md).

## 🛠 Tecnologias Utilizadas

- **Python 3.11** - Linguagem principal
- **pytest** - Framework de testes
- **flake8** - Linter / análise estática
- **GitHub Actions** - CI/CD
- **matplotlib** - Geração de gráficos
- **pandas** - Manipulação de dados
- **requests** - Consultas à API do GitHub

## 👤 Autor

**Kauan Massuia** - Engenharia de Software - Inteli

---

*Projeto desenvolvido como atividade ponderada de análise de pipelines CI/CD.*