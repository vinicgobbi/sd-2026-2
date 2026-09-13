# servidor_multicliente.py — Laboratório da Aula 3 (um servidor, vários clientes)
# Uma THREAD por cliente: o laço principal nunca fica preso em um atendimento.
# Rode em um terminal:  python servidor_multicliente.py
import socket, threading

HOST, PORT = "127.0.0.1", 5000


def atender(conexao, endereco):          # roda em uma thread por cliente
    print(f"[servidor] {endereco} conectou", flush=True)
    while True:
        dado = conexao.recv(1024)
        if not dado:                     # cliente fechou
            break
        conexao.sendall(dado)            # eco: devolve o mesmo
    conexao.close()
    print(f"[servidor] {endereco} saiu", flush=True)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()
print(f"[servidor] ouvindo em {HOST}:{PORT}", flush=True)

while True:
    conexao, endereco = s.accept()       # aceita um cliente...
    threading.Thread(target=atender, args=(conexao, endereco),
                     daemon=True).start()  # ...entrega a uma thread e volta já
