# Aula 7 — Revisão da C1 + Avaliação C1.A1 (17/09/2026)

Dia de prova (C1.A1, 5,0 pts) e de entrega do trabalho C1.A2 (5,0 pts). Sem código novo: abaixo, as respostas das **6 perguntas-chave** da revisão e o gabarito comentado do esquenta.

## As 6 perguntas que você precisa saber responder

1. **Por que TCP difere de UDP?**
   TCP é orientado a conexão: entrega garantida, ordenada, com retransmissão e controle de fluxo — paga isso em latência. UDP envia datagramas sem conexão, sem confirmação nem retransmissão — mais leve e rápido, mas pode perder ou desordenar. Critério: **garantia × latência** (arquivo/página → TCP; áudio/vídeo ao vivo, jogos → UDP). *(Aula 2)*

2. **O que é falha parcial?**
   Parte do sistema falha enquanto o resto continua funcionando — e quem chama muitas vezes não consegue distinguir "o outro lado caiu" de "a rede está lenta". Só existe porque há rede no meio; por isso usamos timeout. *(Aula 1)*

3. **O que uma thread resolve — e qual problema ela cria?**
   Resolve o servidor sequencial travado por um cliente lento: uma thread por conexão libera o laço principal para aceitar o próximo. Cria a **condição de corrida** em dados compartilhados (ex.: contador), resolvida com exclusão mútua (`Lock`) na seção crítica. *(Aula 3)*

4. **Para que serve o arquivo `.proto`?**
   É o **contrato** do serviço gRPC: define mensagens e métodos com tipos. A partir dele se geram stubs de cliente e servidor em várias linguagens, e a serialização é binária (Protocol Buffers) sobre HTTP/2. *(Aula 4)*

5. **O que determina o verbo e o código de status de uma rota REST?**
   O verbo vem da **intenção sobre o recurso**: `GET` lê, `POST` cria, `PUT` substitui, `DELETE` remove (GET/PUT/DELETE idempotentes; POST não). O status vem do **resultado**: 200 OK, 201 Created, 202 Accepted, 404 Not Found, 422 entrada inválida, 5xx erro do servidor. *(Aula 5)*

6. **Por que a inferência de IA muda o desenho do serviço?**
   Carregar o modelo é caro (faz-se 1× no startup) e a inferência é lenta (ms a s), com cold start na 1ª chamada. Segurar o cliente esperando satura o serviço → leva ao processamento **assíncrono com fila** (Aula 8). *(Aula 6)*

## Esquenta — gabarito comentado

| Questão | Tema | Resposta | Por quê |
|---|---|---|---|
| 1 | Áudio ao vivo | **C** | UDP não retransmite: em tempo real, atraso é pior que perda. |
| 2 | Socket e concorrência | **C** (I, II e IV) | III é falsa: condição de corrida ocorre entre threads na mesma máquina. |
| 3 | Idempotência (asserção-razão) | **A** | Por levar ao mesmo estado final, a operação idempotente pode ser retentada. |
| 4 | Microsserviços internos | **B** | gRPC + Protobuf: contrato tipado, binário compacto, HTTP/2. |
| 5 | Vários clientes | **B** | Uma thread por conexão: o cliente lento só afeta a sua thread. |

## Checklist de entrega do C1.A2

- [ ] Clonar do zero e seguir o próprio README — funciona?
- [ ] REST e gRPC devolvem o mesmo resultado para o mesmo texto?
- [ ] O modelo é carregado **uma** vez?
- [ ] Commits ao longo do período (não um único no final)?
