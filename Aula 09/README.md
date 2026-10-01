# Aula 9 — Tempo e ordenação: relógios lógicos (01/10/2026)

## Objetivos

- **Explicar** por que não existe relógio global confiável (clock drift).
- **Aplicar** o relógio de Lamport: `+1` em evento local/envio; `máx(local, carimbo) + 1` no recebimento.
- **Usar** o relógio vetorial para distinguir eventos causais de concorrentes.

## Arquivo

| Arquivo | Descrição |
|---|---|
| [`lamport_sim.py`](./lamport_sim.py) | Simula Lamport e vetorial numa execução e lista os pares concorrentes. **Ampliado para 4 processos e 4 mensagens** (atividade de casa). |

```bash
python lamport_sim.py
```

## A execução ampliada

```
P1:  a ── b(envia m1→P2) ─────────────── j(recebe m3)
P2:  c ──────── d(recebe m1) ── e(envia m2→P3)
P3:  f ─────────────────────── g(recebe m2) ── k(envia m4→P4)
P4:  h ── i(envia m3→P1) ────────────────────────── l(recebe m4)
```

| evento | proc | Lamport | vetor |
|---|---|---|---|
| a | P1 | 1 | [1, 0, 0, 0] |
| b | P1 | 2 | [2, 0, 0, 0] |
| c | P2 | 1 | [0, 1, 0, 0] |
| d | P2 | 3 | [2, 2, 0, 0] |
| e | P2 | 4 | [2, 3, 0, 0] |
| f | P3 | 1 | [0, 0, 1, 0] |
| g | P3 | 5 | [2, 3, 2, 0] |
| h | P4 | 1 | [0, 0, 0, 1] |
| i | P4 | 2 | [0, 0, 0, 2] |
| j | P1 | 3 | [3, 0, 0, 2] |
| k | P3 | 6 | [2, 3, 3, 0] |
| l | P4 | 7 | [2, 3, 3, 3] |

## Explicação escrita — um par causal e um par concorrente

**Par causal: b → l.** O vetor de b, `[2,0,0,0]`, é ≤ o de l, `[2,3,3,3]`, em todas as posições (e diferente), logo b aconteceu antes de l. A cadeia é b envia m1 → d recebe → e envia m2 → g recebe → k envia m4 → l recebe: a informação de b chegou a P4 passando por três mensagens (transitividade).

**Par concorrente: j ‖ l.** Comparando `[3,0,0,2]` com `[2,3,3,3]`: j é maior na posição de P1 (3 > 2) e l é maior nas posições de P2, P3 e P4. Nenhum vetor domina o outro, então nenhum evento influenciou o outro. Repare que Lamport(j) = 3 < Lamport(l) = 7 e, mesmo assim, não há causa: **Lamport ordena, mas não detecta concorrência — o vetorial detecta.**

## Autoavaliação (ENADE)

P2 valia 7 e recebe carimbo 3 → `máx(7, 3) + 1 = 8` → **C**.
