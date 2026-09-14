# app.py — Aula 6 (EAD): o modelo atrás de uma API REST.
# Rode:  uvicorn app:app --port 8000
# Docs:  http://127.0.0.1:8000/docs
#
# Regra de ouro: o modelo é carregado UMA vez, quando o serviço sobe (lifespan),
# e fica em memória. A rota /predict-sync só chama a inferência.
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

import modelo as m

estado = {}                          # o modelo carregado vive aqui


@asynccontextmanager
async def lifespan(app):
    estado["modelo"], dt = m.carregar()                 # 1x, no startup
    print(f"[startup] modelo carregado em {dt:.3f}s")
    yield
    estado.clear()


app = FastAPI(title="Serviço de Inferência", lifespan=lifespan)


class Entrada(BaseModel):
    texto: str


@app.post("/predict-sync")           # síncrono: o cliente espera a inferência
def predict_sync(entrada: Entrada):
    t0 = time.perf_counter()
    sentimento, confianca = m.prever(estado["modelo"], entrada.texto)
    tempo_ms = round((time.perf_counter() - t0) * 1000, 3)
    return {"texto": entrada.texto, "sentimento": sentimento,
            "confianca": confianca, "tempo_ms": tempo_ms}
