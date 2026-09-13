# servidor_grpc.py — Laboratório da Aula 4 (servidor gRPC)
# Antes de rodar, gere os stubs (veja servico.proto).
# Rode:  python servidor_grpc.py
import grpc
from concurrent import futures
import servico_pb2, servico_pb2_grpc


class CalculadoraServicer(servico_pb2_grpc.CalculadoraServicer):
    def Somar(self, request, context):            # implementa a operação do contrato
        return servico_pb2.Resultado(valor=request.a + request.b)


def main():
    # o gRPC atende vários clientes com um POOL DE THREADS (Aula 3)
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servico_pb2_grpc.add_CalculadoraServicer_to_server(CalculadoraServicer(), servidor)
    servidor.add_insecure_port("127.0.0.1:50051")
    servidor.start()
    print("[servidor gRPC] ouvindo em 127.0.0.1:50051", flush=True)
    servidor.wait_for_termination()


if __name__ == "__main__":
    main()
