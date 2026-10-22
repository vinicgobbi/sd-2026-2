# Relatório Raft e resiliência — Aula 11

## Missão 1 — Eleição de líder e quórum

**Com 5 nós, quantos votos formam a maioria? E com 7?**
Maioria = `N // 2 + 1`. Com 5 nós são **3** votos e com 7 nós são **4**. Na simulação com N=7, o voto dividido mostra o limite: o Nó 3 junta só 3 votos (ele e os Nós 6 e 7), porque os Nós 1, 2, 4 e 5 já votaram num concorrente. Como 3 < 4, ninguém é eleito e o mandato termina sem líder.

**Por que cada nó vota no máximo uma vez por mandato? O que isso evita?**
Evita **dois líderes no mesmo mandato** (split-brain). Se cada nó só pode dar um voto, dois candidatos não conseguem ter maioria ao mesmo tempo: duas maiorias de um mesmo grupo sempre têm pelo menos um nó em comum, e esse nó não pode ter votado nos dois. No pior caso ninguém vence (voto dividido) e abre-se um novo mandato, mas nunca há dois líderes.

## Missão 2 — Log replicado, queda do líder e a relação com o CAP

Saídas da versão com **N = 7** ([`raft_sim.py`](./raft_sim.py)):

| Cenário | Nós vivos | Confirmações | Resultado |
|---|---|---|---|
| `x=10` com todos vivos | 7 | 7/7 | COMITADA |
| Líder (Nó 1) cai → Nó 2 eleito no mandato 2 com 6/7 votos; `x=20` | 6 | 6/7 | COMITADA (e `x=10` permanece) |
| Dois nós caem (6 e 7) antes de `y=1` | 5 | 5/7 | COMITADA (5 ≥ 4) |
| Mais dois caem (4 e 5) antes de `y=2` | 3 | 3/7 | **NÃO comitada** (3 < 4) |

**Maioria ↔ lado CP do CAP.** O Raft só confirma uma escrita quando a maioria a gravou. Assim, qualquer maioria futura (inclusive a que eleger o próximo líder) contém pelo menos um nó com aquela entrada, e nada comitado se perde. É por isso que `x=10` sobrevive à troca de líder. O preço aparece no último cenário: com só 3 de 7 nós alcançáveis, o sistema **recusa** a escrita em vez de aceitar algo que pode divergir. Numa partição 4 × 3, só o lado com 4 nós continua aceitando escritas; o lado com 3 fica indisponível. Isso é abrir mão de A para manter C: **Raft é CP**.

## Missão 3 — Timeout, retentativa com backoff e disjuntor

Versão ampliada em [`resiliencia.py`](./resiliencia.py):

- **Os 3 estados** (Cenário 1): fechado → 3 chamadas falham → **aberto** (t3 falha rápido, nem chama o serviço) → após o descanso, **meia-volta** (t4 sonda) → OK → **fechado**.
- **Disjuntor reabrindo** (Cenário 2): o serviço demora mais a voltar. A sondagem de t4 falha, então o disjuntor volta a **aberto** e t5 falha rápido. Em t6 há uma nova meia-volta, a sondagem dá certo e ele fecha.
- **Backoff exponencial:** antes de cada retentativa a chamada espera `1, 2, 4, ...` ticks (`BACKOFF_BASE * 2 ** (tentativa - 1)`). Assim um serviço sobrecarregado ganha fôlego, em vez de receber uma rajada de retentativas imediatas.

**O que acontece sem o disjuntor quando o serviço cai?** No Cenário 3, com o serviço fora do ar por 20 chamadas, **sem disjuntor são 40 batidas** no serviço caído (2 tentativas por chamada) e **com disjuntor são 14**. Sem o disjuntor, cada chamada, com todas as retentativas, insiste num serviço que já está mal. Cada uma segura um worker até o timeout, a fila acumula, e a carga extra atrasa a recuperação do serviço. A falha se propaga em cascata. Com o disjuntor, o sistema falha rápido, libera os workers e só faz uma sondagem de vez em quando.

**Idempotência:** a retentativa só é segura se repetir a operação não duplica o efeito. Uma inferência (ler o texto e devolver o sentimento) é idempotente. Um `POST` que cria um recurso ou cobra um cartão não é, e precisa de uma chave de idempotência para o servidor reconhecer e ignorar a repetição.
