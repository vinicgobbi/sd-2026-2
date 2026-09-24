# pubsub_demo.py — Aula 8 (Desafio): fila × pub/sub, em memória.
#
# FILA: cada mensagem é consumida por UM worker (distribui trabalho).
# PUB/SUB: a mesma mensagem chega a TODOS os assinantes (distribui informação).
#
# Rode:  python pubsub_demo.py
import queue
import threading
import time


class Topico:
    """Pub/sub mínimo: cada assinante tem a sua própria fila."""
    def __init__(self):
        self.assinantes = []

    def assinar(self):
        caixa = queue.Queue()
        self.assinantes.append(caixa)
        return caixa

    def publicar(self, evento):
        for caixa in self.assinantes:
            caixa.put(evento)


def fila_de_trabalho():
    print("FILA — 1 consumidor por mensagem")
    fila = queue.Queue()
    recebidos = {"A": [], "B": [], "C": []}

    def worker(nome):
        while True:
            try:
                recebidos[nome].append(fila.get(timeout=0.2))
                time.sleep(0.05)             # processa a tarefa
            except queue.Empty:
                return

    for i in range(6):
        fila.put(f"tarefa {i}")
    ts = [threading.Thread(target=worker, args=(n,)) for n in recebidos]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    for nome, msgs in recebidos.items():
        print(f"  worker {nome}: {msgs}")
    print(f"  total entregue: {sum(map(len, recebidos.values()))} (cada tarefa uma vez)\n")


def publicar_assinar():
    print("PUB/SUB — todos os assinantes recebem")
    topico = Topico()
    servicos = {nome: topico.assinar() for nome in ("estoque", "notificacao", "relatorio")}
    topico.publicar("pedido 42 concluído")
    for nome, caixa in servicos.items():
        print(f"  {nome:12} recebeu: {caixa.get_nowait()!r}")


if __name__ == "__main__":
    fila_de_trabalho()
    publicar_assinar()
