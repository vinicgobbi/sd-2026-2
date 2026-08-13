import socket
import threading

HOST, PORT = '127.0.0.1', 5000

clientes = []
lock = threading.Lock()

def tratar_cliente(conexao, endereco):
	print(f"[servidor] cliente conectado em: {endereco}", flush=True)
	with lock:
		clientes.append(conexao)
	while True:
		dado = conexao.recv(1024)
		if not dado:
			break
		print(f"[servidor] recebi de {endereco}: {dado.decode()}", flush=True)
		with lock:
			for c in clientes:
				if c is not conexao:
					try:
						c.sendall(dado)
					except OSError:
						pass
	with lock:
		clientes.remove(conexao)
	conexao.close()
	print(f"[servidor] cliente {endereco} desconectado", flush=True)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST,PORT))
s.listen()
print(f"[servidor] ouvindo em {HOST}:{PORT}", flush=True)

while True:
	conexao, endereco = s.accept()
	threading.Thread(target=tratar_cliente, args=(conexao, endereco), daemon=True).start()