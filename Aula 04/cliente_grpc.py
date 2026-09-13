# cliente_grpc.py — Laboratório da Aula 4 (cliente gRPC)
# Rode em OUTRO terminal (com o servidor no ar):  python cliente_grpc.py
import grpc
import servico_pb2, servico_pb2_grpc

with grpc.insecure_channel("127.0.0.1:50051") as canal:
    stub = servico_pb2_grpc.CalculadoraStub(canal)
    resposta = stub.Somar(servico_pb2.Operandos(a=2, b=3))   # parece uma chamada local!
    print("2 + 3 =", resposta.valor)
