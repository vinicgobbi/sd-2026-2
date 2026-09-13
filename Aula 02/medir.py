# medir.py — CASA da Aula 2: mede o round-trip de 100 mensagens.
#
# Antes de rodar, deixe DOIS servidores no ar:
#   - o servidor_eco.py (TCP) na porta 5000  (Aula 2)
#   - o seu eco UDP        na porta 5001
# Depois:  python medir.py
#
# A parte TCP ja esta pronta como MODELO. Complete a parte UDP (TODOs).
import socket
import time

N = 100
HOST = "127.0.0.1"


def medir_tcp(porta=5000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, porta))
    inicio = time.perf_counter()
    for _ in range(N):
        s.sendall(b"x")
        s.recv(1024)
    dt = time.perf_counter() - inicio
    s.close()
    return dt


def medir_udp(porta=5001):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    inicio = time.perf_counter()
    for _ in range(N):
        s.sendto(b"x", (HOST, porta))
        s.recvfrom(1024)
    dt = time.perf_counter() - inicio
    s.close()
    return dt


tcp = medir_tcp()
udp = medir_udp()
print(f"TCP: total {tcp * 1000:7.1f} ms  |  {tcp / N * 1000:.3f} ms/msg")
print(f"UDP: total {udp * 1000:7.1f} ms  |  {udp / N * 1000:.3f} ms/msg")
print("Escreva no medicao.md: qual foi mais rapido e por que (garantias do TCP).")
