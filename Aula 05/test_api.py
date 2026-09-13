# test_api.py — CASA da Aula 5: 3 testes da sua API REST.
#
# Instale:  pip install pytest httpx
# Rode:     pytest test_api.py -v
#
# O 1o teste esta PRONTO, como modelo. Complete os outros dois (TODOs).
from fastapi.testclient import TestClient
from app import app                       # importa o 'app' do seu app.py

cliente = TestClient(app)


def test_criar_devolve_201():             # <-- MODELO pronto
    resposta = cliente.post("/tarefas", json={"titulo": "estudar SD"})
    assert resposta.status_code == 201
    assert resposta.json()["titulo"] == "estudar SD"


def test_listar_devolve_200():
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)


def test_id_inexistente_devolve_404():
    resposta = cliente.get("/tarefas/9999")
    assert resposta.status_code == 404
