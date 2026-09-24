# vazao.py — Aula 8 (Missão 2): mede a vazão da fila com 1, 3 e 6 workers.
#
# Versão em memória da medição do carga.py (sem Redis): o produtor enfileira N
# tarefas e cronometramos até a fila drenar. A "inferência" disputa uma CPU com
# NUCLEOS núcleos (um Semaphore): por isso, a partir de certo número de workers,
# a vazão para de crescer — é o ponto de saturação.
#
# Rode:  python vazao.py          # 50 tarefas (padrão)
#        python vazao.py 100
import queue
import sys
import threading
import time

NUCLEOS = 4                          # capacidade da "máquina"
CUSTO_INFERENCIA = 0.05              # segundos por tarefa
cpu = threading.Semaphore(NUCLEOS)


def inferencia(texto):
    with cpu:                        # só NUCLEOS inferências ao mesmo tempo
        time.sleep(CUSTO_INFERENCIA)
    return "positivo"


def medir(n_tarefas, n_workers):
    fila = queue.Queue()
    resultados = {}
    for i in range(n_tarefas):       # PRODUTOR
        fila.put({"id": i, "texto": f"a tarefa numero {i} foi otima"})

    def worker():
        while True:
            try:
                tarefa = fila.get_nowait()
            except queue.Empty:
                return
            resultados[tarefa["id"]] = inferencia(tarefa["texto"])

    inicio = time.perf_counter()
    workers = [threading.Thread(target=worker) for _ in range(n_workers)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()
    total = time.perf_counter() - inicio
    assert len(resultados) == n_tarefas
    return total


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    print(f"{n} tarefas, {CUSTO_INFERENCIA * 1000:.0f} ms cada, CPU com {NUCLEOS} núcleos\n")
    print("| nº de workers | tempo total (s) | tarefas/s |")
    print("|---|---|---|")
    for n_workers in (1, 3, 6):
        total = medir(n, n_workers)
        print(f"| {n_workers} | {total:.2f} | {n / total:.1f} |")
