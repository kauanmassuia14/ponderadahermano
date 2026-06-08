# Ponderada - Instrumentação de Pipeline CI/CD

Repositório da atividade ponderada sobre análise de pipelines CI/CD com GitHub Actions.

## Estrutura

```
├── .github/workflows/ci.yml     # Pipeline do GitHub Actions
├── src/                          # Código-fonte (3 módulos Python)
├── tests/                        # Testes automatizados (72 testes)
├── scripts/
│   ├── collect_metrics.py        # Coleta métricas via API do GitHub
│   └── generate_charts.py        # Gera gráficos a partir do CSV
├── metrics/                      # CSV e JSON com dados coletados
├── charts/                       # Gráficos gerados
├── RELATORIO.md                  # Relatório técnico
├── requirements-dev.txt          # Dependências de dev/CI
└── setup.cfg                     # Config do flake8
```

## Pipeline

O workflow roda a cada push na `main` com as etapas:

1. Cache de dependências pip
2. Instalação de dependências
3. Lint com flake8
4. Testes com pytest (gera JSON report)
5. Upload de artefatos (resultados + métricas)

## Como reproduzir

```bash
# Clonar e instalar
git clone https://github.com/kauanmassuia14/ponderadahermano.git
cd ponderadahermano
pip install -r requirements-dev.txt

# Rodar testes e lint localmente
pytest tests/ -v
flake8 src/ tests/

# Coletar métricas (precisa de GITHUB_TOKEN)
export GITHUB_TOKEN="seu_token"
python scripts/collect_metrics.py

# Gerar gráficos
python scripts/generate_charts.py
```

## Variações realizadas

Foram feitas 14 execuções com variações controladas (testes falhando, teste lento, sem cache, jobs paralelos, erro de lint, etc). Detalhes no [RELATORIO.md](RELATORIO.md).

## Autor

Kauan Massuia - Engenharia de Computação - Inteli