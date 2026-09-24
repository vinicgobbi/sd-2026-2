# Aula 8 — Mensageria, eventos e API Gateway (24/09/2026)

## Objetivos

- **Diferenciar** comunicação síncrona de assíncrona e saber quando usar cada uma.
- **Processar** tarefas de forma assíncrona com fila e worker (retentativa + dead-letter).
- **Explicar** fila × pub/sub e o papel do API Gateway.

## Arquivos

| Arquivo | Descrição |
|---|---|
| [`fila_demo.py`](./fila_demo.py) | Aquecimento: fila em memória com 3 workers; a tarefa "envenenada" vai para a dead-letter após 3 tentativas. |
| [`vazao.py`](./vazao.py) | Missão 2: mede o tempo para drenar 50 tarefas com 1, 3 e 6 workers. |
| [`worker_resiliente.py`](./worker_resiliente.py) | Missão 3 / TAREFA 5: worker com retentativa até N vezes + dead-letter. |
| [`pubsub_demo.py`](./pubsub_demo.py) | Desafio: a mesma mensagem numa fila (1 consumidor) × num tópico pub/sub (todos recebem). |

Tudo usa só a biblioteca padrão:

```bash
python fila_demo.py
python vazao.py            # ou: python vazao.py 100
python worker_resiliente.py
python pubsub_demo.py
```

## Relatório — tabela de vazão (Missão 2)

50 tarefas, 50 ms de "inferência" cada, máquina simulada com 4 núcleos:

| nº de workers | tempo total (s) | tarefas/s |
|---|---|---|
| 1 | 2,52 | 19,9 |
| 3 | 0,86 | 58,4 |
| 6 | 0,66 | 76,2 |

**Ponto de saturação:** de 1 para 3 workers a vazão quase triplica (escala linear, sem mexer no produtor). De 3 para 6 ela cresce bem menos: só 4 inferências cabem ao mesmo tempo, então os workers extras ficam esperando a CPU. A partir de ~4 workers o gargalo deixa de ser "quantos processam" e passa a ser a capacidade da máquina/modelo.

## Missão 3 — quem sobrevive à queda de quem?

- **Worker cai:** as tarefas ficam guardadas na fila e a fila cresce; ao subir o worker de novo, ela drena. A fila protege contra picos e contra a queda do worker.
- **Fila (Redis) cai:** o `POST /predict` não consegue enfileirar — sem fila não há assíncrono. A fila é um **ponto único de falha** → gancho para replicação e CAP (Aula 10).
- **Tarefa envenenada:** reprocessar para sempre travaria o worker; descartar esconderia o problema. A dead-letter isola a mensagem para análise e o fluxo principal segue.

## Autoavaliação (ENADE)

Fila × pub/sub → **B**: na fila, cada mensagem é consumida por um único consumidor; no pub/sub, a mesma mensagem é entregue a todos os assinantes.
