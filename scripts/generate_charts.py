#!/usr/bin/env python3
"""
Script de geração de gráficos a partir das métricas coletadas.

Lê o arquivo metrics/pipeline_metrics.csv e gera gráficos
na pasta charts/ para análise visual do pipeline CI/CD.

Uso:
    python scripts/generate_charts.py

Autor: Kauan Massuia
Data: Junho 2026
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")  # Backend sem GUI para gerar imagens
import matplotlib.pyplot as plt
import pandas as pd

# Configuração visual dos gráficos
plt.rcParams.update({
    "figure.figsize": (12, 6),
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "figure.facecolor": "white",
    "axes.facecolor": "#f8f9fa",
    "axes.grid": True,
    "grid.alpha": 0.3,
})

CHARTS_DIR = "charts"
CSV_PATH = "metrics/pipeline_metrics.csv"


def carregar_dados():
    """Carrega e prepara os dados do CSV."""
    if not os.path.exists(CSV_PATH):
        print(f"Erro: arquivo {CSV_PATH} não encontrado.")
        print("Execute primeiro: python scripts/collect_metrics.py")
        sys.exit(1)

    df = pd.read_csv(CSV_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.sort_values("run_number")
    print(f"Dados carregados: {len(df)} registros")
    return df


def grafico_tempo_total(df):
    """Gráfico 1: Tempo total do pipeline por execução."""
    fig, ax = plt.subplots(figsize=(14, 6))

    cores = ["#2ecc71" if s == "success" else "#e74c3c"
             for s in df["status"]]

    bars = ax.bar(
        range(len(df)), df["workflow_duration_s"],
        color=cores, edgecolor="white", linewidth=0.5
    )

    ax.set_xlabel("Execução (#Run Number)")
    ax.set_ylabel("Duração Total (segundos)")
    ax.set_title("Tempo Total do Pipeline por Execução")
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(
        [f"#{r}" for r in df["run_number"]],
        rotation=45, ha="right"
    )

    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="#2ecc71", label="Sucesso"),
        Patch(facecolor="#e74c3c", label="Falha"),
    ]
    ax.legend(handles=legend_elements, loc="upper right")

    # Linha de média
    media = df["workflow_duration_s"].mean()
    ax.axhline(y=media, color="#3498db", linestyle="--",
               linewidth=1.5, label=f"Média: {media:.1f}s")
    ax.annotate(f"Média: {media:.1f}s",
                xy=(len(df) - 1, media),
                fontsize=10, color="#3498db",
                fontweight="bold")

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "tempo_total_por_execucao.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ {path}")


def grafico_tempo_por_etapa(df):
    """Gráfico 2: Tempo por etapa (install, lint, test)."""
    fig, ax = plt.subplots(figsize=(14, 6))

    x = range(len(df))
    width = 0.25

    ax.bar([i - width for i in x], df["step_install_s"],
           width, label="Instalação", color="#3498db", alpha=0.85)
    ax.bar(x, df["step_lint_s"],
           width, label="Lint (flake8)", color="#f39c12", alpha=0.85)
    ax.bar([i + width for i in x], df["step_test_s"],
           width, label="Testes (pytest)", color="#9b59b6", alpha=0.85)

    ax.set_xlabel("Execução (#Run Number)")
    ax.set_ylabel("Duração (segundos)")
    ax.set_title("Tempo por Etapa do Pipeline")
    ax.set_xticks(x)
    ax.set_xticklabels(
        [f"#{r}" for r in df["run_number"]],
        rotation=45, ha="right"
    )
    ax.legend()

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "tempo_por_etapa.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ {path}")


def grafico_taxa_sucesso_falha(df):
    """Gráfico 3: Taxa de sucesso e falha."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    contagem = df["status"].value_counts()
    cores_pizza = {"success": "#2ecc71", "failure": "#e74c3c"}
    cores = [cores_pizza.get(s, "#95a5a6") for s in contagem.index]
    labels = [{"success": "Sucesso", "failure": "Falha"}.get(s, s)
              for s in contagem.index]

    ax1.pie(contagem.values, labels=labels, colors=cores,
            autopct="%1.1f%%", startangle=90, textprops={"fontsize": 12})
    ax1.set_title("Distribuição de Status")

    # Barras por execução
    status_num = [1 if s == "success" else 0 for s in df["status"]]
    cores_bar = ["#2ecc71" if s == 1 else "#e74c3c" for s in status_num]
    ax2.bar(range(len(df)), [1] * len(df), color=cores_bar,
            edgecolor="white", linewidth=0.5)
    ax2.set_xlabel("Execução (#Run Number)")
    ax2.set_ylabel("Status")
    ax2.set_title("Status por Execução")
    ax2.set_xticks(range(len(df)))
    ax2.set_xticklabels(
        [f"#{r}" for r in df["run_number"]],
        rotation=45, ha="right"
    )
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(["Falha", "Sucesso"])

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "taxa_sucesso_falha.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ {path}")


def grafico_testes_vs_duracao(df):
    """Gráfico 4: Relação entre quantidade de testes e duração."""
    fig, ax = plt.subplots(figsize=(12, 6))

    # Se test_count for zero, usar step_test_s como proxy
    test_data = df[df["step_test_s"] > 0].copy()

    if len(test_data) < 2:
        test_data = df.copy()

    scatter = ax.scatter(
        test_data["step_test_s"],
        test_data["workflow_duration_s"],
        c=["#2ecc71" if s == "success" else "#e74c3c"
           for s in test_data["status"]],
        s=100, alpha=0.7, edgecolors="white", linewidth=1.5
    )

    # Linha de tendência
    if len(test_data) >= 2:
        import numpy as np
        z = np.polyfit(test_data["step_test_s"],
                       test_data["workflow_duration_s"], 1)
        p = np.poly1d(z)
        x_line = sorted(test_data["step_test_s"])
        ax.plot(x_line, p(x_line), "--", color="#3498db",
                linewidth=2, alpha=0.7, label="Tendência")

    # Labels
    for _, row in test_data.iterrows():
        ax.annotate(f"#{int(row['run_number'])}",
                    (row["step_test_s"], row["workflow_duration_s"]),
                    textcoords="offset points", xytext=(5, 5),
                    fontsize=8, alpha=0.7)

    ax.set_xlabel("Duração dos Testes (segundos)")
    ax.set_ylabel("Duração Total do Pipeline (segundos)")
    ax.set_title("Relação entre Duração dos Testes e Tempo Total do Pipeline")
    ax.legend()

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "testes_vs_duracao.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ {path}")


def grafico_cache_impacto(df):
    """Gráfico 5 (Bônus): Impacto do cache nas dependências."""
    fig, ax = plt.subplots(figsize=(10, 6))

    cache_groups = df.groupby("cache_hit")["step_install_s"].mean()

    if len(cache_groups) >= 2:
        labels_map = {"yes": "Com Cache", "no": "Sem Cache", "unknown": "Desconhecido"}
        labels = [labels_map.get(k, k) for k in cache_groups.index]
        cores = ["#2ecc71" if k == "yes" else "#e74c3c" if k == "no"
                 else "#95a5a6" for k in cache_groups.index]
        ax.bar(labels, cache_groups.values, color=cores,
               edgecolor="white", linewidth=1)
        ax.set_ylabel("Tempo Médio de Instalação (s)")
        ax.set_title("Impacto do Cache na Instalação de Dependências")

        for i, v in enumerate(cache_groups.values):
            ax.text(i, v + 0.5, f"{v:.1f}s", ha="center",
                    fontweight="bold", fontsize=12)
    else:
        ax.text(0.5, 0.5, "Dados insuficientes para comparação de cache",
                ha="center", va="center", transform=ax.transAxes, fontsize=14)
        ax.set_title("Impacto do Cache (dados insuficientes)")

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "cache_impacto.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ {path}")


def grafico_timeline(df):
    """Gráfico 6 (Bônus): Timeline de execuções."""
    fig, ax = plt.subplots(figsize=(14, 6))

    cores = ["#2ecc71" if s == "success" else "#e74c3c"
             for s in df["status"]]

    ax.plot(range(len(df)), df["workflow_duration_s"],
            marker="o", linewidth=2, color="#3498db", alpha=0.7,
            markerfacecolor="white", markeredgewidth=2, markersize=8)

    for i, (_, row) in enumerate(df.iterrows()):
        cor = "#2ecc71" if row["status"] == "success" else "#e74c3c"
        ax.plot(i, row["workflow_duration_s"], "o",
                color=cor, markersize=10, zorder=5)

    ax.set_xlabel("Execução (#Run Number)")
    ax.set_ylabel("Duração Total (segundos)")
    ax.set_title("Timeline de Execuções do Pipeline")
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(
        [f"#{r}" for r in df["run_number"]],
        rotation=45, ha="right"
    )

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "timeline_execucoes.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ {path}")


def main():
    print("=" * 60)
    print("GERAÇÃO DE GRÁFICOS - PIPELINE CI/CD")
    print("=" * 60)

    os.makedirs(CHARTS_DIR, exist_ok=True)
    df = carregar_dados()

    print("\nGerando gráficos...")
    grafico_tempo_total(df)
    grafico_tempo_por_etapa(df)
    grafico_taxa_sucesso_falha(df)
    grafico_testes_vs_duracao(df)
    grafico_cache_impacto(df)
    grafico_timeline(df)

    print(f"\nTodos os gráficos salvos em: {CHARTS_DIR}/")
    print("Concluído!")


if __name__ == "__main__":
    main()
