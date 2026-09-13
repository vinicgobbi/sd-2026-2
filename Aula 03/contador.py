# contador.py — Aula 3: a CONDIÇÃO DE CORRIDA (sem proteção)
#
# "total += 1" são, na verdade, TRÊS passos: LER -> SOMAR -> GRAVAR.
# Se duas threads leem o mesmo valor antes de gravar, uma contagem se perde.
#
# Em CPython o GIL costuma ESCONDER essa corrida no "+= 1". Por isso aqui
# separamos ler/gravar e usamos time.sleep(0) para forçar a troca de thread
# entre os dois passos — assim a corrida fica VISÍVEL e reproduzível.
#
# Rode algumas vezes:  python contador.py   -> o total muda e fica < 4000
import threading, time

total = 0


def soma_muitas():
    global total
    for _ in range(2000):
        atual = total          # LER
        time.sleep(0)          # (troca de thread aqui) — revela a corrida
        total = atual + 1      # GRAVAR


threads = [threading.Thread(target=soma_muitas) for _ in range(2)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("total:", total, "(esperado: 4000)")
