# gerar_stubs.ps1 — gera os stubs gRPC a partir do servico.proto (Windows/PowerShell)
# Uso:  .\gerar_stubs.ps1
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. servico.proto
Write-Host "Stubs gerados: servico_pb2.py e servico_pb2_grpc.py"
