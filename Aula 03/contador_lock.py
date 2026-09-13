# contador_lock.py — Aula 3: a CORREÇÃO (exclusão mútua com lock)
#
# O MESMO código do contador.py, mas o trecho "ler-somar-gravar" fica dentro
# de "with lock:" — a seção crítica. Só uma thread por vez entra ali, então
# nenhuma contagem se perde, mesmo com a troca de thread forçada.
#
# Rode:  python contador_lock.py   -> SEMPRE 4000
import threading, time

total = 0
lock = threading.Lock()          # a trava


def soma_muitas():
    global total
    for _ in range(2000):
        with lock:               # SEÇÃO CRÍTICA: uma thread por vez
            atual = total
            time.sleep(0)
            total = atual + 1


threads = [threading.Thread(target=soma_muitas) for _ in range(2)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("total:", total, "(esperado: 4000)")
