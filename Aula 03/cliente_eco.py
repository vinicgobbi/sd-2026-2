# cliente.py — Laboratório da Aula 3 (cliente interativo do eco)
# Abra VÁRIOS terminais e rode este cliente em cada um, ao mesmo tempo.
# Rode:  python cliente.py
import socket

HOST, PORT = "127.0.0.1", 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Conectado. Digite mensagens (ou 'sair'):")
while True:
    msg = input("> ")
    if msg == "sair":
        break
    s.sendall(msg.encode())
    eco = s.recv(1024)
    print("eco:", eco.decode())
s.close()
