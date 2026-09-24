# worker_resiliente.py — Aula 8 (Missão 3 / TAREFA 5): retentativa + dead-letter.
#
# O worker do fila_demo.py, reorganizado como uma função reutilizável:
# tenta processar; se falhar, reenfileira até MAX_TENTATIVAS; persistindo a
# falha, manda a mensagem para a dead-letter (isola para análise, sem travar a
# fila). O texto "ENVENENADA" provoca o erro de propósito.
#
# Rode:  python worker_resiliente.py
import queue
import threading
import time

MAX_TENTATIVAS = 3


def processa(tarefa):
    if tarefa["texto"] == "ENVENENADA":
        raise ValueError("entrada inválida")
    time.sleep(0.02)                             # a "inferência"
    return {"status": "pronto", "sentimento": "positivo"}


def worker(nome, fila, resultados, dead_letter):
    while True:
        try:
            tarefa = fila.get(timeout=1)
        except queue.Empty:
            return
        try:
            resultados[tarefa["id"]] = processa(tarefa)
            print(f"[{nome}] processando {tarefa['id']} -> pronto", flush=True)
        except Exception as erro:
            tarefa["tentativas"] = tarefa.get("tentativas", 0) + 1
            tarefa["ultimo_erro"] = str(erro)
            if tarefa["tentativas"] < MAX_TENTATIVAS:
                fila.put(tarefa)                 # RETENTATIVA
                print(f"[{nome}] {tarefa['id']} falhou ({erro}), "
                      f"tentativa {tarefa['tentativas']}/{MAX_TENTATIVAS}", flush=True)
            else:
                dead_letter.append(tarefa)       # DEAD-LETTER
                print(f"[{nome}] {tarefa['id']} -> DEAD-LETTER", flush=True)


def rodar(textos, n_workers=3):
    fila, resultados, dead_letter = queue.Queue(), {}, []
    for i, texto in enumerate(textos):
        fila.put({"id": i, "texto": texto})
    workers = [threading.Thread(target=worker, args=(f"w{i}", fila, resultados, dead_letter))
               for i in range(n_workers)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()
    return resultados, dead_letter


if __name__ == "__main__":
    textos = [f"doc {i}" for i in range(6)] + ["ENVENENADA"]
    resultados, dead_letter = rodar(textos)
    print(f"\nprontos: {len(resultados)} | dead-letter: {[t['id'] for t in dead_letter]}")
