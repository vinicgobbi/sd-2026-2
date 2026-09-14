# Aula 6 — IA como serviço distribuído (EAD)

## Objetivos

- **Dominar** o vocabulário mínimo de IA: modelo, inferência, embedding, token, LLM e cold start.
- **Servir** um modelo atrás de uma API REST, carregando-o **uma única vez** no startup.
- **Medir** latência e cold start de um serviço de inferência.

## Arquivos

| Arquivo | Descrição |
|---|---|
| [`modelo.py`](./modelo.py) | Classificador de sentimento de brinquedo. `carregar()` é caro (simula 1,5s de leitura do disco); `prever()` é a inferência. |
| [`app.py`](./app.py) | API FastAPI que carrega o modelo no `lifespan` (1×) e expõe `POST /predict-sync`. |
| [`medir_tempos.py`](./medir_tempos.py) | Chama `/predict-sync` 10 vezes e mede o tempo de ida-e-volta. |
| [`test_api.py`](./test_api.py) | Testes: resposta da rota, validação (422) e o modelo carregado só uma vez. |

### Como rodar

```bash
pip install -r ../requirements.txt
uvicorn app:app --port 8000        # log: [startup] modelo carregado em 1.500s
python medir_tempos.py             # em outro terminal
pytest test_api.py -v
```

## Relatório — tempos medidos (Passo 3)

Custo de carga do modelo, pago **uma vez** no startup: `1.500s`.

| Chamada | Tempo (ida-e-volta) |
|---|---|
| 1ª (cold start) | 13,9 ms |
| média das 9 seguintes (warm) | 1,9 ms |

**Leitura:** a 1ª chamada é a mais lenta (o ambiente ainda está aquecendo: conexão nova, primeiras alocações). As seguintes ficam baixas e estáveis porque o modelo já está em memória — a regra de ouro. Se o modelo fosse carregado a cada requisição, **toda** chamada pagaria os 1,5s. Com um modelo pesado (LLM), mesmo a inferência warm levaria centenas de ms ou segundos, e segurar o cliente esperando vira um mau desenho → fila e processamento assíncrono (Aula 8).

## Autoavaliação (ENADE)

Serviço lento porque o modelo é carregado do disco a cada requisição → **B**: carregar o modelo uma única vez, na inicialização, mantendo-o em memória.
