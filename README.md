# Dashboard de Service Desk — SLA e Atendimento (Power BI)

Dashboard operacional para acompanhar o desempenho de uma equipe de suporte de TI: volume de chamados, cumprimento de SLA, categorias e chamados em risco. **Todos os dados são sintéticos** (gerados por `gerar_dados.py`), inspirados no tipo de indicador usado em operações de service desk.

## Perguntas de negócio que o dashboard responde
1. Quantos chamados entram e quantos são resolvidos por dia/mês?
2. Qual o % de chamados resolvidos dentro do SLA, e como isso evolui?
3. Quais categorias concentram volume e estouram mais o SLA?
4. Quais chamados em aberto estão perto de vencer ou sem atualização?
5. Como está a carga da equipe, sem usar volume como único critério de desempenho?

> Decisão de design: o dashboard **não rankeia técnicos como melhores ou piores só por volume**. Quantidade de chamados não mede qualidade; por isso a visão por técnico mostra volume junto de % SLA e tempo médio, como apoio à gestão e não como ranking.

## Dados (`/dados`)
| Arquivo | Conteúdo |
|---|---|
| `chamados.csv` | 1.200 chamados fictícios: abertura, categoria, técnico, VIP, SLA (h), tempo de resolução, status |
| `tecnicos.csv` | 12 técnicos fictícios e equipes |
| `calendario.csv` | Tabela calendário 2026 |

Regenerar: `python gerar_dados.py` (requer pandas e numpy).

## Modelo de dados
Esquema estrela: `chamados` (fato) ligada a `tecnicos` por `tecnico_id` e a `calendario` por `abertura[date]` → `calendario[data]`.

## Medidas DAX
```DAX
Total Chamados = COUNTROWS(chamados)

Resolvidos = CALCULATE([Total Chamados], chamados[status] = "Resolvido")

Em Andamento = CALCULATE([Total Chamados], chamados[status] = "Em andamento")

Dentro SLA = CALCULATE([Total Chamados], chamados[dentro_sla] = TRUE())

% SLA = DIVIDE([Dentro SLA], [Resolvidos])

Tempo Médio Resolução (h) = AVERAGE(chamados[horas_resolucao])

Média Diária de Chamados =
DIVIDE([Total Chamados], DISTINCTCOUNT(chamados[abertura_data]))

Sem Atualização (3+ dias) =
CALCULATE([Em Andamento], chamados[dias_sem_atualizacao] >= 3)

Chamados VIP em Aberto =
CALCULATE([Em Andamento], chamados[usuario_vip] = TRUE())
```
Em Power Query, crie `abertura_data` = parte data de `abertura` e defina `dentro_sla` como Verdadeiro/Falso.

## Estrutura das páginas
1. **Visão Geral**: cartões (Total, Resolvidos, % SLA, Tempo Médio, Em Andamento), linha de volume mensal, barras por categoria.
2. **SLA**: % SLA por categoria e mês, matriz de calor categoria × mês, lista de chamados em risco.
3. **Equipe**: tabela por técnico com volume, % SLA e tempo médio (sem ordenar como ranking).
4. **Alertas**: chamados VIP em aberto e sem atualização, com filtro por equipe.

## Prints
Adicione em `docs/` e referencie aqui:
```md
![Visão geral](docs/visao-geral.png)
```

## Tecnologias
Power BI · DAX · Power Query · Python (pandas) para geração dos dados

## Autor
**Artur Martins** · [LinkedIn](https://www.linkedin.com/in/artur-martins) · [GitHub](https://github.com/arturmartinsgo)
