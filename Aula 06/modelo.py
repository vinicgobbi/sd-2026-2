# modelo.py — Aula 6 (EAD): um "modelo" de sentimento de brinquedo.
#
# Não é IA de verdade: é um léxico de palavras positivas/negativas. O que
# importa para a disciplina é o COMPORTAMENTO de um modelo servido:
#   - carregar() é CARO (simula ler um arquivo grande do disco);
#   - prever() é a INFERÊNCIA (barata, depois de carregado).
import time

POSITIVAS = {"otimo", "ótimo", "bom", "boa", "excelente", "rapido", "rápido", "adorei", "gostei"}
NEGATIVAS = {"ruim", "pessimo", "péssimo", "lento", "horrivel", "horrível", "odiei", "demorado"}
CUSTO_CARGA = 1.5                    # segundos para "ler o modelo do disco"


def carregar():
    """Operação cara: deve rodar UMA vez, no startup do serviço."""
    t0 = time.perf_counter()
    time.sleep(CUSTO_CARGA)          # simula ler e preparar um arquivo grande
    modelo = {"positivas": POSITIVAS, "negativas": NEGATIVAS}
    return modelo, time.perf_counter() - t0


def prever(modelo, texto):
    """Inferência: texto -> (sentimento, confiança)."""
    palavras = texto.lower().split()
    pos = sum(p in modelo["positivas"] for p in palavras)
    neg = sum(p in modelo["negativas"] for p in palavras)
    if pos == neg:
        return "neutro", 0.5
    confianca = round(0.5 + 0.5 * abs(pos - neg) / len(palavras), 2)
    return ("positivo" if pos > neg else "negativo"), confianca
