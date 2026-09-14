# medir_tempos.py — Aula 6 (EAD): mede o tempo da rota /predict-sync.
#
# Antes, suba o serviço (nesta pasta, com o .venv ativo):
#   uvicorn app:app --port 8000
# Depois, em outro terminal:
#   python medir_tempos.py
#
# Objetivo: observar o "cold start" (a 1a chamada é a mais lenta) e o tempo "warm".
import time
import requests

# use 127.0.0.1 (e nao "localhost"): no Windows, "localhost" via requests pode
# custar ~1-2s por causa da resolucao IPv6/proxy — atrapalharia a medicao.
BASE = "http://127.0.0.1:8000"
TEXTO = "o atendimento foi otimo e muito rapido"

tempos = []
for i in range(10):
    t0 = time.perf_counter()
    r = requests.post(f"{BASE}/predict-sync", json={"texto": TEXTO}, timeout=30)
    dt = (time.perf_counter() - t0) * 1000        # ida-e-volta, em ms
    tempos.append(dt)
    print(f"chamada {i + 1:2d}: {dt:7.1f} ms  ->  {r.json().get('sentimento')}")

print(f"\n1a chamada:            {tempos[0]:.1f} ms")
print(f"media das seguintes:   {sum(tempos[1:]) / len(tempos[1:]):.1f} ms")
print("O modelo foi carregado no startup -> as requisicoes ficam rapidas e estaveis.")
print("Anote esses numeros no relatorio.md.")
