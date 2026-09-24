# fila_demo.py — Aula 8: a fila como amortecedor (demo em memória, sem Docker)
#
# Mostra os conceitos SEM precisar de Redis: um produtor enfileira tarefas e
# VÁRIOS workers (threads da Aula 3) consomem — um por mensagem. Uma tarefa
# "envenenada" falha sempre e, após 3 tentativas, vai para a dead-letter.
#
# Rode:  python fila_demo.py
import queue
import threading
import time

fila = queue.Queue()          # a fila de tarefas
resultados = {}               # id -> resultado pronto
dead_letter = []              # tarefas que falharam demais
MAX_TENTATIVAS = 3


def produtor(n=8):
    for i in range(n):
        fila.put({"id": i, "texto": f"doc {i}", "tentativas": 0})
    fila.put({"id": 99, "texto": "ENVENENADA", "tentativas": 0})   # falha sempre
    print(f"[produtor] enfileirou {n + 1} tarefas", flush=True)


def worker(nome):
    while True:
        try:
            tarefa = fila.get(timeout=2)        # bloqueia até chegar tarefa
        except queue.Empty:
            return                              # fila vazia por 2s -> encerra
        try:
            if tarefa["texto"] == "ENVENENADA":
                raise ValueError("entrada inválida")
            time.sleep(0.05)                    # simula a inferência
            resultados[tarefa["id"]] = "ok"
            print(f"[{nome}] processou tarefa {tarefa['id']}", flush=True)
        except Exception as erro:
            tarefa["tentativas"] += 1
            if tarefa["tentativas"] < MAX_TENTATIVAS:
                fila.put(tarefa)                # RETENTATIVA: volta para a fila
                print(f"[{nome}] falhou {tarefa['id']} ({erro}) — tentativa "
                      f"{tarefa['tentativas']}, reenfileira", flush=True)
            else:
                dead_letter.append(tarefa)      # DEAD-LETTER: isola para análise
                print(f"[{nome}] {tarefa['id']} -> DEAD-LETTER", flush=True)


produtor(8)
# suba mais workers e veja a carga se dividir (escalabilidade = + workers)
workers = [threading.Thread(target=worker, args=(f"w{i}",), daemon=True)
           for i in range(3)]
for w in workers:
    w.start()
for w in workers:
    w.join()

print(f"\nprocessadas: {len(resultados)} | na dead-letter: {len(dead_letter)}")
