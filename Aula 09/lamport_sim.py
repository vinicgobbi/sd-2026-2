# lamport_sim.py — Aula 9: simula relógios de Lamport e vetorial numa execução.
#
# Não precisa de rede: descrevemos a ORDEM real dos eventos e o programa aplica
# as regras. Ele imprime, para cada evento, o relógio de Lamport e o vetorial,
# e no fim aponta um PAR CONCORRENTE (nem um causou o outro).
#
# Atividade de casa: ampliada para 4 processos (P4) e 4 mensagens (m1..m4).
#
# Rode:  python lamport_sim.py
processos = ["P1", "P2", "P3", "P4"]
idx = {p: i for i, p in enumerate(processos)}

# Execução: a ordem real dos eventos. tipo ∈ {local, send, recv}.
execucao = [
    ("P1", "local", "a", None),
    ("P1", "send",  "b", "m1"),   # P1 envia m1 para P2
    ("P2", "local", "c", None),
    ("P2", "recv",  "d", "m1"),   # P2 recebe m1
    ("P2", "send",  "e", "m2"),   # P2 envia m2 para P3
    ("P3", "local", "f", None),
    ("P3", "recv",  "g", "m2"),   # P3 recebe m2
    ("P4", "local", "h", None),
    ("P4", "send",  "i", "m3"),   # P4 envia m3 para P1
    ("P1", "recv",  "j", "m3"),   # P1 recebe m3
    ("P3", "send",  "k", "m4"),   # P3 envia m4 para P4
    ("P4", "recv",  "l", "m4"),   # P4 recebe m4
]

lamport = {p: 0 for p in processos}
vetor = {p: [0] * len(processos) for p in processos}
carimbo_l, carimbo_v = {}, {}     # relógio que viaja junto com cada mensagem
eventos = []

for proc, tipo, rotulo, msg in execucao:
    if tipo in ("local", "send"):
        lamport[proc] += 1                       # regra: evento local -> +1
        vetor[proc][idx[proc]] += 1
        if tipo == "send":                       # envia o relógio atual junto
            carimbo_l[msg] = lamport[proc]
            carimbo_v[msg] = list(vetor[proc])
    else:  # recv
        lamport[proc] = max(lamport[proc], carimbo_l[msg]) + 1   # MÁXIMO + 1
        vetor[proc] = [max(a, b) for a, b in zip(vetor[proc], carimbo_v[msg])]
        vetor[proc][idx[proc]] += 1
    eventos.append((rotulo, proc, lamport[proc], list(vetor[proc])))

print(f"{'evento':7}{'proc':6}{'Lamport':9}vetor")
for rotulo, proc, l, v in eventos:
    print(f"{rotulo:<7}{proc:<6}{l:<9}{v}")


def causou(v1, v2):                              # v1 'aconteceu antes' de v2?
    return all(a <= b for a, b in zip(v1, v2)) and v1 != v2


print("\nPares concorrentes (nem um causou o outro):")
for i in range(len(eventos)):
    for j in range(i + 1, len(eventos)):
        vi, vj = eventos[i][3], eventos[j][3]
        if not causou(vi, vj) and not causou(vj, vi):
            print(f"  {eventos[i][0]}({eventos[i][1]})  ||  {eventos[j][0]}({eventos[j][1]})")
