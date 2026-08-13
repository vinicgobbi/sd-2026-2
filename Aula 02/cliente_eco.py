import socket
import threading

HOST, PORT = "127.0.0.1", 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP
s.connect((HOST, PORT))                        # CONECTA no servidor
print("Conectado. Digite mensagens (ou 'sair'):")

def receber():
    while True:
        dado = s.recv(1024)                     # RECEBE mensagens do outro cliente
        if not dado:
            print("\n[cliente] servidor encerrou a conexão", flush=True)
            break
        print(f"\noutro cliente: {dado.decode()}\n> ", end="", flush=True)

threading.Thread(target=receber, daemon=True).start()

while True:
    msg = input("> ")
    if msg == "sair":
        break
    s.sendall(msg.encode())                    # ENVIA bytes
    print(f"voce: {msg}")
s.close()