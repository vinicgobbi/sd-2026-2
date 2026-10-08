# Relatório CAP — Aula 10

## (a) O experimento

Duas réplicas do mesmo dado (`A` recebe as escritas; `B` atende leituras do outro lado da rede) simuladas em [`replicas_sim.py`](./replicas_sim.py). A "rede" entre elas é a flag `particionado` (`particionar()` / `curar()`).

1. **Rede OK:** `preco=10` é escrito em A e replicado para B. Leitura em B devolve `v1` — as cópias concordam.
2. **Partição:** a rede é cortada e duas escritas chegam só em A (`preco=20` e `preco=30`). B fica parado em `v1`.
3. **Escolha do CAP:** a mesma leitura em B, sob partição, no modo AP devolve o valor velho; no modo CP recusa com 503.
4. **Cura:** a rede volta, B copia o estado de A (`v3`) e as réplicas convergem — consistência eventual.

### Momento da divergência

```
    ## rede PARTICIONADA: A e B nao se falam ##
    A <- "preco=20" (v2)
    B  x  NAO recebe (particao) - continua em v1
    >>> MOMENTO DA DIVERGENCIA: A=v2  B=v1 <<<
    A <- "preco=30" (v3)
    B  x  NAO recebe (particao) - continua em v1
    leitura em A: "preco=30" (v3)       | leitura em B: "preco=10" (v1) DESATUALIZADO (AP: prioriza Disponibilidade)
    => A esta 2 versoes a frente de B: um cliente em cada replica ve um preco diferente.
```

A divergência começa na **versão v2**, a primeira escrita que não cruzou a partição. Com a escrita extra, A terminou a partição **2 versões à frente** de B: no mesmo instante, um cliente em A via `preco=30` e outro em B via `preco=10`.

### Escolha AP × CP pelo tipo do dado (Missão 3)

A função `ler(clusters, dado)` consulta `MODO_POR_DADO` e lê de B no modo correspondente. Sob a **mesma** partição:

```
    saldo     [CP] -> 503 INDISPONIVEL (CP: prioriza Consistencia)
    estoque   [CP] -> 503 INDISPONIVEL (CP: prioriza Consistencia)
    curtidas  [AP] -> "42" (v1) DESATUALIZADO (AP: prioriza Disponibilidade)
    catalogo  [AP] -> "v1" (v1) DESATUALIZADO (AP: prioriza Disponibilidade)
```

## (b) Duas justificativas

**CP — saldo de conta / carteira digital.** Mostrar um saldo velho pode levar o cliente a gastar um dinheiro que já não tem, ou a ver uma transferência "sumir". O custo de um dado errado (prejuízo, perda de confiança, problema regulatório) é muito maior que o de responder "tente de novo em instantes". Sob partição, a réplica desatualizada **recusa** (503): abre mão de A para preservar C.

**AP — contador de curtidas de uma publicação.** Se a réplica mostra 42 curtidas em vez de 43 por alguns segundos, ninguém é prejudicado, e quando a rede volta o número converge. Já derrubar o feed inteiro por causa de uma curtida perdida seria uma péssima experiência. Sob partição, a réplica **responde** com o valor possivelmente velho: abre mão de C para preservar A (consistência eventual).

## Decisão para o C2.A2 (índice vetorial do RAG)

Se o índice vetorial do serviço de recuperação fosse replicado, a busca seria **AP**. Um índice sem os documentos ingeridos nos últimos segundos ainda devolve trechos relevantes, e a resposta só perde um pouco de completude. Recusar a busca deixaria o RAG inteiro fora do ar. A ingestão (escrita no índice) pode reconciliar depois que a partição curar.
