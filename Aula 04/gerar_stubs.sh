#!/usr/bin/env bash
# gerar_stubs.sh — gera os stubs gRPC a partir do servico.proto (Linux/macOS)
# Uso:  ./gerar_stubs.sh
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. servico.proto
echo "Stubs gerados: servico_pb2.py e servico_pb2_grpc.py"
