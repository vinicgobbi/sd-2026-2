# carga.py — CASA da Aula 3: teste de carga do servidor multicliente.
#
# Deixe o servidor_multicliente.py no ar (porta 5000) e rode:
#   python carga.py
#
# A logica de UM cliente ja esta pronta. Complete os TODOs: dispare N clientes
# em THREADS ao mesmo tempo e meca o tempo total (o assunto da aula).
import socket
import threading
import time

HOST, PORT = "127.0.0.1", 5000
N = 50                       # experimente depois com 10, 50, 100
MENSAGENS = 5

tempos = []                  # cada cliente anota aqui quanto levou


def um_cliente(i):
    t0 = time.perf_counter()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    for _ in range(MENSAGENS):
        s.sendall(b"ola")
        s.recv(1024)
    s.close()
    tempos.append(time.perf_counter() - t0)


threads = []
for i in range(N):
    threads.append(threading.Thread(target=um_cliente, args=(i,)))

inicio = time.perf_counter()
for t in threads:
    t.start()
for t in threads:
    t.join()
total = time.perf_counter() - inicio

media = sum(tempos) / len(tempos) if tempos else 0
print(f"N={N} clientes | tempo total: {total * 1000:.1f} ms | "
      f"media por cliente: {media * 1000:.1f} ms")
print("Repita com N=10, 50, 100 e anote no relatorio_concorrencia.md.")
