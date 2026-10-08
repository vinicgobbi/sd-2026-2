# Aula 10 — Replicação, consistência e o teorema CAP (08/10/2026)

## Objetivos

- **Explicar** por que replicamos dados e qual é o custo (manter as cópias iguais).
- **Enunciar** o CAP: sob partição, só dá para garantir C **ou** A.
- **Distinguir** consistência forte de eventual e escolher a adequada ao tipo de dado.

## Arquivos

| Arquivo | Descrição |
|---|---|
| [`replicas_sim.py`](./replicas_sim.py) | Duas réplicas e uma partição. Ampliado com escrita extra sob partição, leitura A × B lado a lado e a regra `ler(dado)` que escolhe AP/CP pelo tipo do dado. |
| [`relatorio_cap.md`](./relatorio_cap.md) | O experimento, o momento da divergência e as justificativas CP e AP. |

```bash
python replicas_sim.py
```

## Resumo

| | CP | AP |
|---|---|---|
| Leitura na réplica desatualizada | recusa (503) | responde o valor antigo |
| Abre mão de | A | C |
| Dados típicos | saldo, estoque, senha | curtidas, catálogo, feed |

"CA" só existe sem rede: num sistema distribuído a partição é inevitável, então a escolha real é CP × AP.

## Autoavaliação (ENADE)

Carteira digital que recusa a leitura de saldo sob partição → **B**: CP, prioriza a consistência e abre mão da disponibilidade.
