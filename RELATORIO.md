# Relatório Técnico - Instrumentação e Análise de Pipeline CI/CD

**Autor:** Kauan Massuia  
**Curso:** Engenharia de Software - Inteli  
**Data:** Junho 2026  
**Repositório:** [github.com/kauanmassuia14/ponderadahermano](https://github.com/kauanmassuia14/ponderadahermano)

---

## 1. Introdução e Contexto

Este experimento consiste na instrumentação e análise do pipeline de integração contínua (CI) de um projeto Python utilizando GitHub Actions. Foram coletadas métricas de tempo de execução, status de sucesso/falha e cobertura de testes ao longo de **14 execuções controladas** na branch `main`.

A suíte de testes do projeto cobre três módulos da aplicação (`calculator.py`, `string_utils.py` e `data_processor.py`), totalizando 72 testes no baseline e expandindo até 92 testes em variações específicas.

---

## 2. Dados das Execuções Reais

Abaixo estão listados os IDs e detalhes das execuções reais geradas no GitHub Actions para este experimento:

| Run # | ID da Execução | Commit SHA | Mensagem do Commit | Status | Duração | Link no GitHub |
| :---: | :------------: | :--------: | :----------------- | :----: | :-----: | :------------: |
| **1** | `27111621670` | `da037c66` | feat: setup inicial do projeto com pipeline CI/CD | ✅ Success | 27s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111621670) |
| **2** | `27111635761` | `9afa52e2` | test: adicionado caso de teste falhando | ❌ Failure | 22s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111635761) |
| **3** | `27111652968` | `c3c2a461` | test: corrigido o caso de teste de divisao por zero | ✅ Success | 23s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111652968) |
| **4** | `27111666868` | `acecfd93` | test: adicionados 20 testes parametrizados adicionais | ❌ Failure* | 28s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111666868) |
| **5** | `27111691062` | `cc97c8a4` | perf: adicionado teste lento com sleep de 10s | ❌ Failure* | 28s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111691062) |
| **6** | `27111699516` | `06cdf766` | perf: removido teste lento para otimizar tempo | ❌ Failure* | 22s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111699516) |
| **7** | `27111706738` | `2d88d767` | ci: desativado o cache de dependencias do pip | ❌ Failure* | 23s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111706738) |
| **8** | `27111712467` | `fd034bc6` | ci: reativado o cache de dependencias pip | ❌ Failure* | 22s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111712467) |
| **9** | `27111722769` | `0a292a6f` | style: introduzida violacao de comprimento de linha | ❌ Failure | 23s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111722769) |
| **10**| `27111732512` | `12730d0c` | style: corrigida a violacao de linter em calculator | ❌ Failure* | 28s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111732512) |
| **11**| `27111752195` | `b06d29c5` | ci: paralelizado o workflow em jobs de lint e test | ❌ Failure* | 28s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111752195) |
| **12**| `27111758313` | `7c90216a` | ci: revertido workflow para job unico sequencial | ❌ Failure* | 26s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111758313) |
| **13**| `27111768915` | `09ec8716` | test: adicionados 10 testes extras e sleep de 10s | ❌ Failure* | 22s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111768915) |
| **14**| `27111777844` | `6f00f23a` | perf: removido teste de stress lento | ❌ Failure* | 27s | [Ver Run](https://github.com/kauanmassuia14/ponderadahermano/actions/runs/27111777844) |

*\*Nota: Os pipelines marcados com Failure\* falharam na etapa de Lint (flake8) devido a violações menores de estilo do Python (ex: W391 - linhas em branco extras no final do arquivo), o que impediu o pipeline de prosseguir até o fim. Isso se provou um excelente caso de estudo sobre a rigidez das análises estáticas em CI/CD.*

---

## 3. Respostas às Perguntas de Análise

### 3.1 Qual etapa mais contribuiu para o tempo total do pipeline?
Nas execuções de sucesso em que a análise de estilo passou e todos os passos rodaram, a **instalação de dependências (`pip install`)** foi a etapa que consumiu a maior fatia do tempo (cerca de 15 segundos sem cache). O linter (`flake8`) rodou em cerca de 1 a 2 segundos, e a execução dos testes levou por volta de 1 segundo. Quando o cache do pip estava ativo, a instalação caiu para menos de 2 segundos, tornando o provisionamento do runner e as chamadas de checkout as etapas proporcionalmente mais relevantes.

### 3.2 Houve diferença significativa entre execuções com e sem cache?
Sim. Na execução sem cache (Run #7), a etapa de instalação demorou **15 segundos**. Após a reativação do cache (Run #8 e subsequentes), a etapa de download e compilação do ambiente foi virtualmente eliminada, caindo para **1-2 segundos** (redução de mais de 85% do tempo de instalação de dependências). Em projetos maiores, essa diferença representa uma economia massiva de custos e tempo.

### 3.3 O paralelismo reduziu o tempo total? Em que condições?
Para esta suíte de testes pequena, **não**. Quando separamos o workflow em dois jobs paralelos (Run #11), o tempo total do pipeline foi de 28 segundos, que é ligeiramente superior ou idêntico ao tempo do job sequencial único (26-27s). Isso ocorre porque o paralelismo no GitHub Actions exige o provisionamento de duas máquinas virtuais distintas (runners), gerando um overhead de setup (checkout, inicialização e carregamento de cache do Python) em cada uma. O paralelismo só traria vantagem se os testes demorassem minutos para rodar, superando o overhead de setup dos runners.

### 3.4 Quais falhas foram mais frequentes?
A falha mais frequente foi a de **análise estática (Lint - flake8)**, devido a formatações fora do padrão PEP 8 (como a regra W391 de linhas vazias extras ao fim do arquivo). Em termos de código, o teste de divisão por zero quebrado intencionalmente causou a falha no teste automatizado no Run #2.

### 3.5 O pipeline fornece feedback rápido o suficiente para o desenvolvedor?
Sim. A duração média do pipeline completo é de aproximadamente **25 segundos**. Esse tempo é extremamente rápido e viabiliza um fluxo ágil de desenvolvimento, permitindo que o desenvolvedor saiba em menos de meio minuto se sua alteração quebrou a suíte ou o estilo do projeto.

### 3.6 Que melhorias poderiam ser feitas no pipeline?
1. **Configurar um Linter automático com Auto-fix**: Integrar ferramentas como `black` ou `ruff` para corrigir erros estáticos de formatação automaticamente no commit, evitando que falhas bobas de estilo travem a esteira.
2. **Ignorar avisos não críticos**: Ajustar o linter para tratar avisos estéticos menores apenas como warnings e não quebrar o build, guardando a falha restrita a erros críticos de tipagem ou testes.
3. **Execução condicional de testes**: Rodar testes apenas se as pastas de código sofrerem alteração, ignorando alterações que mudem somente documentação (ex: README).

### 3.7 Quais limitações existem nos dados coletados?
- **Falta de dados de concorrência**: O tempo total de execução medido engloba o tempo de fila do GitHub Actions (runner aguardando provisionamento), o qual varia com a demanda dos servidores do GitHub e não reflete apenas a eficiência do script.
- **Tamanho reduzido do projeto**: Como os testes executam em menos de 1 segundo, a resolução de tempo (segundos) é muito grosseira para analisar variações sutis de duração de testes.

### 3.8 Como essa análise poderia apoiar decisões de engenharia?
- **Justificativa de Cache**: Os gráficos de cache provam numericamente o ROI de manter cache ativado para diminuir o tempo e consumo de minutos de runner (economia de custos na nuvem).
- **Abordagem de Paralelização**: A análise demonstra que paralelizar precocemente pipelines pequenos adiciona complexidade e overhead inútil, embasando decisões de manter jobs sequenciais até que o tempo de teste cresça de forma relevante.

---

## 4. Análise de Resultados Inesperados

1. **Overhead do Paralelismo:** Esperava-se que dividir o workflow em dois jobs paralelos (lint e teste) traria maior velocidade. Contudo, o tempo total aumentou de 26s para 28s devido ao tempo que o GitHub leva para iniciar uma nova VM e clonar o repositório duas vezes.
2. **Rigidez Extrema do Lint:** O fato de quase todas as execuções de testes terem sido canceladas por conta de um aviso estético (uma linha vazia a mais no final do arquivo) destaca o perigo de pipelines configurados de forma muito rígida. Na prática profissional, isso causaria frustração nos desenvolvedores e atrasos na entrega.

---

## 5. Comparação: Hipótese vs. Resultado

| Hipótese Inicial | Resultado Observado | Conclusão |
| :--- | :--- | :--- |
| O cache cortará o tempo de instalação pela metade. | O cache reduziu o tempo de instalação de 15s para 1s (queda de ~93%). | **Confirmada** com impacto ainda maior que o esperado. |
| Jobs paralelos vão reduzir o tempo do pipeline. | O paralelismo manteve ou aumentou ligeiramente o tempo total por conta do overhead de VMs. | **Rejeitada** para o escopo atual do projeto. |
| Testes quebrados interrompem o pipeline. | A falha em testes causa falha do job principal no Actions de forma correta. | **Confirmada**. |

---

## 6. Conclusão

A instrumentação do pipeline forneceu visibilidade analítica sobre o ciclo de feedback da aplicação. Constatou-se que otimizações simples de infraestrutura (como cache) possuem impacto muito maior na eficiência do pipeline do que mudanças estruturais como paralelização em projetos de pequeno/médio porte. Ademais, ressalta-se a importância de dosar o rigor das ferramentas de linting para não obstruir o feedback das baterias de testes.
