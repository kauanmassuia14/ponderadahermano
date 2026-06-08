#!/usr/bin/env python3
"""
Script de coleta de métricas do pipeline CI/CD via GitHub API.

Uso:
    export GITHUB_TOKEN="seu_token_aqui"
    python scripts/collect_metrics.py

Autor: Kauan Massuia
Data: Junho 2026
"""

import csv
import json
import os
import sys
from datetime import datetime

import requests

OWNER = "kauanmassuia14"
REPO = "ponderadahermano"
API_BASE = f"https://api.github.com/repos/{OWNER}/{REPO}"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def calc_duracao(inicio_str, fim_str):
    """Calcula duração em segundos entre dois timestamps ISO 8601."""
    if not inicio_str or not fim_str:
        return 0.0
    inicio = datetime.fromisoformat(inicio_str.replace("Z", "+00:00"))
    fim = datetime.fromisoformat(fim_str.replace("Z", "+00:00"))
    return round((fim - inicio).total_seconds(), 2)


def buscar_runs():
    """Busca todas as execuções do workflow."""
    runs = []
    page = 1
    while True:
        url = f"{API_BASE}/actions/runs?per_page=100&page={page}"
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            print(f"Erro ao buscar runs: {resp.status_code} - {resp.text}")
            sys.exit(1)
        data = resp.json()
        batch = data.get("workflow_runs", [])
        if not batch:
            break
        runs.extend(batch)
        page += 1
    print(f"Total de workflow runs encontrados: {len(runs)}")
    return runs


def buscar_jobs(run_id):
    """Busca os jobs de uma execução específica."""
    url = f"{API_BASE}/actions/runs/{run_id}/jobs"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        return []
    return resp.json().get("jobs", [])


def processar_runs(runs):
    """Processa todas as runs e extrai métricas."""
    registros = []
    for i, run in enumerate(runs):
        run_id = run["id"]
        print(f"  [{i+1}/{len(runs)}] Run #{run['run_number']} (ID: {run_id})")

        wf_start = run.get("run_started_at", run.get("created_at", ""))
        wf_end = run.get("updated_at", "")
        wf_dur = calc_duracao(wf_start, wf_end)
        sha = run.get("head_sha", "")[:8]
        msg = run.get("display_title", "")
        msg = msg.replace("\n", " ").strip()[:100]
        status = run.get("conclusion", run.get("status", "unknown"))

        jobs = buscar_jobs(run_id)
        if not jobs:
            registros.append({
                "run_id": run_id, "run_number": run["run_number"],
                "commit_sha": sha, "commit_message": msg, "status": status,
                "workflow_duration_s": wf_dur, "job_name": "N/A",
                "job_duration_s": 0, "step_install_s": 0, "step_lint_s": 0,
                "step_test_s": 0, "test_count": 0, "test_failures": 0,
                "timestamp": wf_start, "cache_hit": "unknown",
            })
            continue

        for job in jobs:
            j_dur = calc_duracao(job.get("started_at", ""), job.get("completed_at", ""))
            steps = job.get("steps", [])
            s_install = s_lint = s_test = 0
            cache_hit = "unknown"
            for s in steps:
                nm = s.get("name", "").lower()
                dur = calc_duracao(s.get("started_at", ""), s.get("completed_at", ""))
                if "install" in nm or "dependenc" in nm:
                    s_install = dur
                elif "lint" in nm or "flake" in nm:
                    s_lint = dur
                elif "test" in nm and "upload" not in nm and "metric" not in nm:
                    s_test = dur
                elif "cache" in nm:
                    cache_hit = "yes" if s.get("conclusion") == "success" else "no"

            registros.append({
                "run_id": run_id, "run_number": run["run_number"],
                "commit_sha": sha, "commit_message": msg, "status": status,
                "workflow_duration_s": wf_dur, "job_name": job.get("name", "unknown"),
                "job_duration_s": j_dur, "step_install_s": s_install,
                "step_lint_s": s_lint, "step_test_s": s_test,
                "test_count": 0, "test_failures": 0,
                "timestamp": wf_start, "cache_hit": cache_hit,
            })
    return registros


def salvar(registros, csv_path, json_path):
    """Salva registros em CSV e JSON."""
    if not registros:
        print("Nenhum registro.")
        return
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=registros[0].keys())
        w.writeheader()
        w.writerows(registros)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2, ensure_ascii=False)
    print(f"\nCSV salvo em: {csv_path}")
    print(f"JSON salvo em: {json_path}")
    print(f"Total de registros: {len(registros)}")


def main():
    print("=" * 60)
    print("COLETA DE MÉTRICAS DO PIPELINE CI/CD")
    print(f"Repositório: {OWNER}/{REPO}")
    print("=" * 60)

    if not TOKEN:
        print("\nAVISO: GITHUB_TOKEN não definido.")
        print("Limite de 60 req/hora sem autenticação.")
        print("Use: export GITHUB_TOKEN='seu_token'\n")

    print("\nBuscando workflow runs...")
    runs = buscar_runs()
    if not runs:
        print("Nenhuma execução encontrada.")
        sys.exit(0)

    print("\nProcessando métricas...")
    registros = processar_runs(runs)

    salvar(registros, "metrics/pipeline_metrics.csv", "metrics/pipeline_metrics.json")

    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    total = len(set(r["run_id"] for r in registros))
    ok = sum(1 for r in registros if r["status"] == "success")
    fail = sum(1 for r in registros if r["status"] == "failure")
    print(f"  Execuções: {total} | Sucessos: {ok} | Falhas: {fail}")
    duracoes = [r["workflow_duration_s"] for r in registros if r["workflow_duration_s"] > 0]
    if duracoes:
        print(f"  Duração média: {sum(duracoes)/len(duracoes):.1f}s")
        print(f"  Min: {min(duracoes):.1f}s | Max: {max(duracoes):.1f}s")


if __name__ == "__main__":
    main()
