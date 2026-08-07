# Aula 1 — 06/08/2026

## Objetivos

- **Explicar** o que é um sistema distribuído e por que quase todo software hoje é um.
- **Reconhecer** o desafio que só existe quando há rede no meio: a **falha parcial**.
- **Deixar o ambiente pronto:** Python, VS Code, Git e GitHub (VM a partir de amanhã).

## Demonstração: falha parcial

Um servidor de eco que demora a responder e um cliente com timeout, para observar na prática o que acontece quando a rede (ou o outro lado) falha no meio da comunicação.

| Arquivo | Descrição |
|---|---|
| [`servidor_eco.py`](./servidor_eco.py) | Recebe uma mensagem, simula 15s de processamento e devolve o eco. |
| [`cliente_eco.py`](./cliente_eco.py) | Envia `"oi"` e aguarda a resposta com timeout de 10s. |

### Como rodar

1. Em um terminal, inicie o servidor:

   ```bash
   python servidor_eco.py
   ```

2. Em outro terminal, inicie o cliente:

   ```bash
   python cliente_eco.py
   ```

3. Enquanto o cliente aguarda a resposta, derrube o servidor com `Ctrl+C` no terminal dele e observe o erro reportado pelo cliente (timeout ou conexão resetada).
