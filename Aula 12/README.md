# Aula 12 — Revisão da C2 + Avaliação C2.A1 (29/10/2026)

Dia de prova (C2.A1, 5,0 pts) e de entrega do trabalho C2.A2 — RAG distribuído (5,0 pts). Sem código novo: abaixo, o resumo da revisão, as respostas das **6 perguntas-chave** e o gabarito comentado do esquenta.

## O caminho da C2

**A pergunta da C2:** como vários serviços se coordenam e permanecem consistentes e de pé, apesar de falhas?

| Aula | Problema | Ferramenta |
|---|---|---|
| [8](../Aula%2008/) | serviços acoplados e síncronos | **desacoplar**: fila/worker, pub/sub, API Gateway |
| [9](../Aula%2009/) | não existe "agora" comum | **ordenar**: Lamport e relógio vetorial |
| [10](../Aula%2010/) | cópias divergem sob partição | **escolher**: CAP, CP × AP |
| [11](../Aula%2011/) | concordar e sobreviver a falhas | **concordar/resistir**: Raft (quórum) + timeout, retry, disjuntor |

## Resumo por aula

**Aula 8 — Mensageria.** Síncrono: o cliente espera travado. Assíncrono: o cliente entrega a tarefa, recebe um `id` na hora e busca o resultado depois. A **fila** é um amortecedor: desacopla quem produz de quem consome, absorve picos e escala com mais workers sem mexer no produtor. Mensagem que falha demais vai para a **dead-letter** (nem retentar para sempre, nem perder). **Fila** = 1 consumidor por mensagem (distribui trabalho); **pub/sub** = todos os assinantes recebem (distribui informação). O **API Gateway** é a porta única que centraliza auth, rate limit e log. Acrescentar campo é seguro; remover/renomear exige nova versão (`/v2`).

**Aula 9 — Relógios lógicos.** Relógios físicos têm *clock drift*, por isso o carimbo de hora pode inverter a ordem real. Troca-se "quando" por "o que veio antes" (**causalidade**). A → B quando: mesmo processo e A antes, ou A é o envio e B o recebimento da mesma mensagem, ou por transitividade. Sem ligação entre eles: **concorrentes** (A ‖ B).
- **Lamport:** `+1` em evento local/envio; no recebimento, `máx(local, carimbo) + 1`. Garante que A → B ⇒ L(A) < L(B), mas a **recíproca não vale**: não distingue concorrência.
- **Vetorial:** um contador por processo; no recebimento, máximo posição a posição e depois `+1` na própria posição. Se um vetor é ≤ o outro em tudo, há causalidade; se nenhum domina, os eventos são concorrentes.

**Aula 10 — Replicação e CAP.** Replicar dá disponibilidade, desempenho e durabilidade; o preço é manter as cópias iguais. **CAP:** sob partição (P, inevitável em rede real) não dá para ter C e A juntas.
- **CP:** recusa (503) para não servir dado velho. Ex.: saldo, estoque, senha (bancos relacionais, etcd, ZooKeeper).
- **AP:** responde com dado possivelmente velho. Ex.: curtidas, catálogo, feed (Cassandra, DynamoDB, DNS).
- **Consistência forte:** toda leitura vê a última escrita. **Eventual:** as cópias convergem quando as escritas param ("eventual" não é "nunca").

**Aula 11 — Consenso e resiliência.** Consenso: todos decidem o mesmo valor, e esse valor foi proposto por alguém. **Raft:** um líder ordena e replica; tudo gira em torno de mandatos; cada nó vota uma vez por mandato. Eleger e comitar exigem **quórum = N/2 + 1** (5 → 3; 7 → 4). Se o líder cai, abre-se novo mandato e o que já foi comitado permanece. O lado sem maioria para de aceitar escritas, por isso **Raft é CP**. As três defesas de uma chamada remota são **timeout** (não esperar para sempre), **retry com backoff** (tentar de novo esperando cada vez mais) e **disjuntor** (fechado → aberto após N falhas → meia-volta após descanso → fechado se a sondagem dá certo, aberto se falha). Retentar só é seguro com **idempotência** (ou chave de idempotência).

## As 6 perguntas que você precisa saber responder

1. **Quando usar comunicação assíncrona (fila) em vez de síncrona — e o que a fila resolve?**
   Quando o processamento é lento ou chega em rajadas (ex.: inferência de IA) e segurar o cliente esperando saturaria o serviço. A fila desacopla o recebimento do processamento: a API responde rápido com um `id`, picos se acumulam em vez de derrubar o serviço e a vazão escala com mais workers. *(Aula 8)*

2. **Por que carimbo de hora não ordena eventos distribuídos? O que o Lamport faz?**
   Cada máquina tem seu relógio, que deriva (clock drift), e sincronizar pela rede tem atraso variável. Assim, comparar horas pode inverter a ordem real. O Lamport troca a hora por um contador causal: `+1` a cada evento e `máx(local, carimbo) + 1` ao receber, garantindo que a causa tenha número menor que o efeito. *(Aula 9)*

3. **O que o relógio vetorial detecta que o de Lamport não distingue?**
   **Concorrência.** Com Lamport, L(A) < L(B) não prova que A causou B. Com vetores: se um é ≤ o outro em todas as posições há causalidade; se cada um é maior em alguma posição, os eventos são concorrentes. Essa é a base para detectar conflitos entre réplicas. *(Aula 9)*

4. **Enuncie o CAP: sob partição, o que se escolhe — e o que é consistência eventual?**
   Com dados replicados, durante uma partição não se garantem consistência e disponibilidade ao mesmo tempo. Escolhe-se **CP** (recusar e preservar o dado certo) ou **AP** (responder com dado possivelmente velho). Consistência eventual é o lado AP: as cópias podem divergir por um tempo, mas convergem quando as escritas param. "CA" só existe sem rede. *(Aula 10)*

5. **O que é quórum no Raft e por que ele é um sistema CP?**
   Quórum é a maioria (N/2 + 1) necessária para eleger um líder e para comitar uma entrada. Duas maiorias sempre se cruzam, então nunca há dois líderes no mesmo mandato e nada comitado se perde. Sob partição, o lado sem maioria para de aceitar escritas: abre mão de A para manter C. *(Aula 11)*

6. **Quais as 3 defesas de uma chamada remota — e por que idempotência é pré-condição da retentativa?**
   Timeout, retentativa (com backoff) e disjuntor. A retentativa repete uma operação que talvez já tenha sido executada (a resposta é que se perdeu). Se ela não for idempotente, repetir duplica o efeito, como cobrar duas vezes. Por isso: operação idempotente ou chave de idempotência. *(Aula 11)*

## Esquenta — gabarito comentado

| Questão | Tema | Resposta | Por quê |
|---|---|---|---|
| 1 | Pico no serviço de IA | **B** | A fila desacopla recebimento e processamento, absorve picos e escala com +workers. Não torna nada instantâneo nem consistente. |
| 2 | Lamport (local 5, carimbo 9) | **C** = 10 | `máx(5, 9) + 1 = 10`. Quem esquece o +1 marca 9; quem soma marca 14. |
| 3 | CAP (asserção-razão) | **A** | As duas são verdadeiras e a razão (cópias não se coordenam) justifica a asserção. |
| 4 | Raft 5 réplicas, partição 3 × 2 | **C** | Só o lado com 3 forma maioria (3 de 5) e aceita escritas; o de 2 fica indisponível → CP. |
| 5 | Retry gerou cobrança duplicada | **B** | Criar pagamento não é idempotente: use uma chave de idempotência antes de retentar. |

## Pegadinhas favoritas da prova

- **"O sistema é CA"** → em rede real a partição é inevitável; a escolha é CP ou AP.
- **"Retry resolve tudo"** → só com idempotência; senão duplica efeito.
- **"Carimbo de hora ordena eventos"** → clock drift; use relógio lógico.
- **"Dois líderes no mesmo mandato"** → impossível no Raft: um voto por nó por mandato + maioria.
- **"Lamport menor ⇒ causou"** → não; só o vetorial distingue concorrência.

## Checklist de entrega do C2.A2 (RAG distribuído)

- [ ] Três microsserviços — ingestão, recuperação e geração — rodando e se comunicando?
- [ ] Comunicação via REST/gRPC e mensageria onde faz sentido?
- [ ] Chamada ao LLM protegida (timeout + retry + disjuntor)?
- [ ] Clona do zero e segue o README? Commits ao longo do período?

Rubrica: arquitetura 1,5 · comunicação 1,5 · resiliência 1,0 · execução reproduzível 1,0. A sofisticação do modelo de IA não pontua.
