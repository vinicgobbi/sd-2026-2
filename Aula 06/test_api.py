# test_api.py — Aula 6: testes do serviço de inferência.
#
# Rode:  pytest test_api.py -v
from unittest.mock import patch

from fastapi.testclient import TestClient

import modelo
from app import app


def test_predict_sync_positivo():
    with TestClient(app) as cliente:             # o "with" dispara o startup
        r = cliente.post("/predict-sync", json={"texto": "o atendimento foi otimo"})
    assert r.status_code == 200
    assert r.json()["sentimento"] == "positivo"


def test_predict_sync_sem_texto_devolve_422():
    with TestClient(app) as cliente:
        r = cliente.post("/predict-sync", json={})
    assert r.status_code == 422


def test_modelo_carregado_uma_vez():             # a regra de ouro
    with patch.object(modelo, "carregar", wraps=modelo.carregar) as espiao:
        with TestClient(app) as cliente:
            for _ in range(5):
                cliente.post("/predict-sync", json={"texto": "bom"})
    assert espiao.call_count == 1
