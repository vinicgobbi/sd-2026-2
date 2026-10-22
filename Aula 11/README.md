# Aula 11 — Consenso (Raft) e resiliência (22/10/2026)

## Objetivos

- **Explicar** o problema do consenso e o papel da maioria (quórum = N/2 + 1).
- **Descrever** o Raft: eleição de líder por mandato e log replicado com commit por maioria.
- **Blindar** uma chamada remota com timeout, retentativa (com backoff) e disjuntor, apoiada em idempotência.

## Arquivos

| Arquivo | Descrição |
|---|---|
| [`raft_sim.py`](./raft_sim.py) | Eleição de líder e log replicado. Ampliado para **N = 7** com cenários em que a escrita comita com 2 nós caídos e não comita sem maioria. |
| [`resiliencia.py`](./resiliencia.py) | Timeout + retentativa + disjuntor. Ampliado com **backoff exponencial**, disjuntor **reabrindo** e comparação com/sem disjuntor. |
| [`relatorio_raft.md`](./relatorio_raft.md) | Respostas sobre quórum, relação maioria ↔ CP e a análise do disjuntor. |

```bash
python raft_sim.py
python resiliencia.py
```

## Disjuntor — os 3 estados

```
FECHADO --(N falhas seguidas)--> ABERTO --(descanso)--> MEIA-VOLTA --(sondagem OK)--> FECHADO
                                    ^                        |
                                    +----(sondagem falha)----+
```

## Autoavaliação (ENADE)

Raft com 5 réplicas particionado em 3 × 2 → **C**: só o lado com 3 nós aceita escritas, pois só ele forma maioria (3 de 5).
